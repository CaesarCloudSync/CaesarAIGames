import hashlib
import logging
import os
import sys
import time
import urllib

from typing import Any, Optional
from urllib.parse import urlparse
import redis
import requests
from tqdm.auto import tqdm
from CaesarAIEmail import CaesarAIEmail
from CaesarAIGames.constants import USER_AGENT
from CaesarAIGames.providers.gdrive import get_url_filename_drive
from CaesarAIGames.utils import get_pylogger
import math

log = get_pylogger(__name__)

class CaesarAIGamesTools:
    @staticmethod
    def extract_filename_steamunlocked(url):
        filename = url.split("&")[-1].split("=")[-1]
        return filename
    def extract_filename_steamrip(self):
        pass
class CaesarAIGames:
    def __init__(self) -> None:
        self.r = redis.Redis(host="redis")
    def download(
        self,
        url: str,
        folder: str = None,
        filename: Optional[str] = None,
        session: requests.Session = requests.Session(),
        key: Optional[str] = None,
        proxy: str = None,
        md5: Optional[str] = None,
        sha256: Optional[str] = None,
        max_redirect_hops: int = 3,
        verify: Optional[bool] = None,
        timeout: int = 60,
        retry_max: int = 500,
        sleep_max: int = 120,
        chunk_size: int = 1024,
        show_progress: bool = True,
        logging_level: int = logging.INFO,
    ) :
        """Download a file from a url and place it in folder. Supports robust downloads with resuming,
        connection error handling, proxies, authentication, and more.
        Args:
            url (str): URL to download file from
            folder (str): Directory to place downloaded file in
            filename (str, optional): Name to save the file under. If None, use the basename of the URL
            session (requests.Session, optional): Session to use for HTTP requests.
            key (str, optional): authentication key in the form username:password
            proxy (str, optional): Proxy URL.
            md5 (str, optional): MD5 checksum of the download. If None, do not check
            sha256 (str, optional): SHA256 checksum of the download. If None, do not check
            max_redirect_hops (int, optional): Maximum number of redirects to follow
            verify (bool, optional): Whether to verify SSL certificates
            timeout (int, optional): Timeout for HTTP requests
            retry_max (int, optional): Maximum number of retries
            sleep_max (int, optional): Maximum number of seconds to sleep between retries
            chunk_size (int, optional): Number of bytes to read into memory at once
            show_progress (bool, optional): Whether to show a progress bar
            logging_level (int, optional): Logging level
        """
        # Set logging level
        log.setLevel(logging_level)

        # If folder is None, use current directory
        if folder is None:
            log.info("folder is None, using current directory")
            folder = os.getcwd()

        # Expand redirect hops if needed
        url = self._get_redirect_url(url, max_hops=max_redirect_hops)

        # Additional session configuration
        if key:
            session.auth = tuple(key.split(":", 2))
        if proxy:
            session.proxies = {"http": proxy, "https": proxy}

        # Try to get Google Drive url and if it exists, use it
        url_drive, filename_drive = get_url_filename_drive(url, session, verify)

        # Expand folder and filename
        folder = os.path.expanduser(folder)
        if not filename and not url_drive:
            response = session.head(url, allow_redirects=True)
            content_disposition = response.headers.get("Content-Disposition")
            if content_disposition:
                filename = content_disposition.split(";")[-1]
            else:
                filename = os.path.basename(urlparse(response.url).path)
        elif url_drive:
            url = url_drive
            filename = filename_drive if not filename else filename

        fpath = os.path.join(folder, filename)
        os.makedirs(folder, exist_ok=True)

        # Check if file is already present locally
        if md5 is not None or sha256 is not None and self.check_integrity(fpath, md5, sha256):
            log.info("Using downloaded and verified file: " + fpath)
            self.r.hset(f"current-download:",filename,"already exists using md5")
            

        # Get file size
        try:
            downloaded = os.path.getsize(fpath)
        except FileNotFoundError:
            downloaded = 0
        size = int(session.get(url, stream=True).headers["Content-Length"])
        if downloaded == size:
            log.info("File %s already downloaded", filename)
            self.r.hset(f"current-download:",filename,"file already downloaded")
        elif downloaded > size:
            log.warning(
                "File %s may be corrupted. It is recommended to re-try downloading it."
                % filename
            )
            self.r.hset(f"current-download:",filename,"file may be corrupted")

        log.info("Downloading %s to %s (%s)", url, filename, self.format_bytes(size))

        mode = "ab"  # append to file if it exists
        sleep = 10
        tries = 0
        headers = {"Range": "bytes=%d-" % downloaded, "User-Agent": USER_AGENT}

        # Main loop: download the file in chunks with retries and resume on failure
        notification_dict = {"not_10":"","not_20":"","not_30":"","not_40":"","not_50":"","not_60":"","not_70":"","not_80":"","not_90":"","not_100":""}
        while tries < retry_max:
            r = self.robust_wrapper(session.get, retry_max, sleep_max)(
                url,
                stream=True,
                verify=verify,
                headers=headers,
                timeout=timeout,
            )
            try:
                r.raise_for_status()

                with tqdm(
                    total=size,
                    unit_scale=True,
                    unit_divisor=1024,
                    unit="B",
                    initial=downloaded,
                    disable=not show_progress,
                ) as pbar:
                    with open(fpath, mode) as f:
                        for chunk in r.iter_content(chunk_size=chunk_size):
                            if chunk:
                                f.write(chunk)
                                downloaded += len(chunk)
                                progress = str(((downloaded / size) *100))
                                self.r.hset(f"current-download:",filename.replace("/media/amari/SSD T7/steamunlockedgames/",""),progress)
                                if notification_dict.get(f"not_{int(math.floor(float(progress)))}") == "":
                                    game_name = filename.replace("/media/amari/SSD T7/steamunlockedgames/","").replace(".zip","")
                                    CaesarAIEmail.send(**{"email":"amari.lawal@gmail.com","subject":f"{game_name} - Progress: {progress}%","message":f"{game_name} - Progress: {progress}%"})
                                    notification_dict[f"not_{int(math.floor(float(progress)))}"] = "sent"
                                #print(((downloaded / size) *100))
                                # TODO Store redis progress here
                                #yield str(((downloaded / size) *100))
                                pbar.update(len(chunk))

            except requests.exceptions.ConnectionError as e:
                log.error("Download interrupted: %s" % (e,))
            finally:
                r.close()

            if downloaded >= size:
                break

            log.error(
                "Download incomplete, downloaded %s / %s"
                % (self.format_bytes(downloaded), self.format_bytes(size))
            )
            log.warning("Sleeping %s seconds" % (sleep,))
            time.sleep(sleep)
            mode = "ab"

            downloaded = os.path.getsize(fpath)
            sleep *= 1.5
            if sleep > sleep_max:
                sleep = sleep_max
            headers = {"Range": "bytes=%d-" % downloaded, "User-Agent": USER_AGENT}
            tries += 1
            log.warning("Resuming from downloaded %s" % (self.format_bytes(downloaded),))

        ## TODO: check this part. For certain small files, it may be a false positive
        # if downloaded != size and size > 5000:  # small files may raise false positive
        #     raise Exception(
        #         "Download failed: downloaded %s / %s"
        #         % (format_bytes(downloaded), format_bytes(size))
        #     )

        if md5 is not None or sha256 is not None:
            if not self.check_integrity(fpath, md5, sha256):
                raise RuntimeError("File not found or corrupted.")
            else:
                log.info("File integrity verified!")
        self.r.set(f"current-download:{filename}-result","finished")


    def robust_wrapper(self,call, retry_max=500, sleep_max=120):
        def retriable(code, reason):
            if code in [
                requests.codes.internal_server_error,
                requests.codes.bad_gateway,
                requests.codes.service_unavailable,
                requests.codes.gateway_timeout,
                requests.codes.too_many_requests,
                requests.codes.request_timeout,
            ]:
                return True

            return False

        def wrapped(*args, **kwargs):
            tries = 0
            while tries < retry_max:
                try:
                    r = call(*args, **kwargs)
                except (
                    requests.exceptions.ConnectionError,
                    requests.exceptions.ReadTimeout,
                ) as e:
                    r = None
                    log.warning(
                        "Recovering from connection error [%s], attempts %s of %s",
                        e,
                        tries,
                        retry_max,
                    )

                if r is not None:
                    if not retriable(r.status_code, r.reason):
                        return r
                    try:
                        log.warning(r.json()["reason"])
                    except Exception:
                        pass
                    log.warning(
                        "Recovering from HTTP error [%s %s], attempts %s of %s",
                        r.status_code,
                        r.reason,
                        tries,
                        retry_max,
                    )

                tries += 1

                log.warning("Retrying in %s seconds", sleep_max)
                time.sleep(sleep_max)
                log.info("Retrying now...")

        return wrapped


    def calculate_md5(self,fpath: str, chunk_size: int = 1024 * 1024) -> str:
        # Setting the `usedforsecurity` flag does not change anything about the functionality, but indicates that we are
        # not using the MD5 checksum for cryptography. This enables its usage in restricted environments like FIPS. Without
        # it torchvision.datasets is unusable in these environments since we perform a MD5 check everywhere.
        if sys.version_info >= (3, 9):
            md5 = hashlib.md5(usedforsecurity=False)
        else:
            md5 = hashlib.md5()
        with open(fpath, "rb") as f:
            for chunk in iter(lambda: f.read(chunk_size), b''):
                md5.update(chunk)
        return md5.hexdigest()

    def calculate_sha256(self,fpath: str, chunk_size: int = 1024 * 1024) -> str:
        if sys.version_info >= (3, 9):
            sha256_hash = hashlib.sha256(usedforsecurity=False)
        else:
            sha256_hash = hashlib.sha256()
        with open(fpath, 'rb') as f:
            for chunk in iter(lambda: f.read(chunk_size), b''):
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest()

    def _get_redirect_url(self,url: str, max_hops: int = 3) -> str:
        initial_url = url
        headers = {"Method": "HEAD", "User-Agent": USER_AGENT}

        for _ in range(max_hops + 1):
            with urllib.request.urlopen(
                urllib.request.Request(url, headers=headers)
            ) as response:
                if response.url == url or response.url is None:
                    return url

                url = response.url
        else:
            raise RecursionError(
                f"Request to {initial_url} exceeded {max_hops} redirects. The last redirect points to {url}."
            )


    def check_md5(self,fpath: str, md5: str, **kwargs: Any) -> bool:
        return md5 == self.calculate_md5(fpath, **kwargs)

    def sha256_checksum(self,fpath: str, sha256: str, **kwargs: Any) -> bool:
        return sha256 == self.calculate_sha256(fpath, **kwargs)

    def check_integrity(self,fpath: str, md5: Optional[str] = None, sha256: Optional[str] = None) -> bool:
        if not os.path.isfile(fpath):
            return False
        if md5 is None and sha256 is None:
            return True
        if md5 is not None and sha256 is None:
            return self.check_md5(fpath, md5)
        if md5 is None and sha256 is not None:
            return self.sha256_checksum(fpath, sha256)

    def format_bytes(self,num_bytes):
        units = ["", "K", "M", "G", "T", "P"]
        unit_index = 0
        bytes_remaining = num_bytes
        while bytes_remaining >= 1024:
            bytes_remaining /= 1024.0
            unit_index += 1
        return f"{int(bytes_remaining * 10 + 0.5) / 10.0}{units[unit_index]}"
