import zipfile
import zlib
import os
from tqdm import tqdm
doc = "/media/amari/SSD T7/steamunlockedgames/Sekiro.Shadows.Die.Twice.v1.06.zip"
#doc = "/media/amari/SSD T7/steamunlockedgames/Kingdom.Come.Deliverance.v1.9.6.Incl.ALL.DLC.zip"
from os import fspath
from pathlib import Path
from shutil import copyfileobj
from zipfile import ZipFile
from tqdm.auto import tqdm  # could use from tqdm.gui import tqdm
from tqdm.utils import CallbackIOWrapper

def extractall(fzip, dest, desc="Extracting"):
    """zipfile.Zipfile(fzip).extractall(dest) with progress"""
    dest = Path(dest).expanduser()
    with ZipFile(fzip) as zipf, tqdm(
        desc=desc, unit="B", unit_scale=True, unit_divisor=1024,
        total=sum(getattr(i, "file_size", 0) for i in zipf.infolist()),
    ) as pbar:
        for i in zipf.infolist():
            if not getattr(i, "file_size", 0):  # directory
                zipf.extract(i, fspath(dest))
            else:
                with zipf.open(i) as fi, open(fspath(dest / i.filename), "wb") as fo:
                    copyfileobj(CallbackIOWrapper(pbar.update, fi), fo)

#with open(doc,"rb") as zf:
extractall(doc,"/media/amari/SSD T7/steamunlockedgames/Sekiro.Shadows.Die.Twice.v1.06_Test")