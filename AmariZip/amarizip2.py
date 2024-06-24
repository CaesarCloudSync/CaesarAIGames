import zipfile
import zlib
import os
from tqdm import tqdm
doc = "/home/amari/Desktop/CaesarAIGames/AmariZip/sample-zip-file.zip"
#doc = "/media/amari/SSD T7/steamunlockedgames/Kingdom.Come.Deliverance.v1.9.6.Incl.ALL.DLC.zip"
with zipfile.ZipFile(doc) as zf:
     for member in tqdm(zf.infolist(), desc='Extracting '):
         try:
             print(member)
             zf.extract(member, "Kingdom.Come.Deliverance.v1.9.6.Incl.ALL.DLC")
         except zipfile.error as e:
            print(e)