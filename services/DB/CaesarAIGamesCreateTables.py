from services.DB.CaesarAIGamesCRUD import CaesarAIGamesCRUD
from services.Models import Settings,Backup
class CaesarAIGamesCreateTables:
    @staticmethod
    def create(caesaraigmscrud :CaesarAIGamesCRUD):
        caesaraigmscrud.create_table(Settings.fields_to_tuple(),Settings.SETTINGSDATATYPES,Settings.SETTINGSTABLENAME)
        caesaraigmscrud.create_table(Backup.fields_to_tuple(),Backup.BACKUPDATATYPES,Backup.BACKUPTABLENAME)
