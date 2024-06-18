source_path = "/media/amari/SSD T7/steamunlockedgames/SIFU.v1.27.Incl.ALL.DLC.zip"
target_path = "/media/amari/SSD T7/steamunlockedgames/SIFU.v1.27.Incl.ALL.DLC_PI"
from zipfile import ZipFile

class ZipFileCustom(ZipFile):
    """ Custom ZipFile class with a callback on extractall. """

    def extractall(self, path=None, members=None, pwd=None, fn_progress=None):
        if members is None:
            members = self.namelist()

        if path is None:
            path = os.getcwd()
        else:
            path = os.fspath(path)

        for index, member in enumerate(members):
            print(member)
            if fn_progress:
                fn_progress(len(members), index + 1)
            self._extract_member(member, path, pwd)
def calculate_percentage(total: int, current: int):
    percent = float(current) / total
    percent = round(percent * 100)
    return percent
with ZipFileCustom(source_path) as zfc:
    zfc.extractall(target_path, fn_progress=lambda total, current: print(f'{calculate_percentage(total, current)} %'))