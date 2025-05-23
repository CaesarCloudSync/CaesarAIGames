from services.DB.CaesarAIGamesCRUD import CaesarAIGamesCRUD
from services.Models import Settings
class CaesarAIGamesCreateTables:
    @staticmethod
    def create(caesaraigmscrud :CaesarAIGamesCRUD):
        caesaraigmscrud.create_table(Settings.fields_to_tuple(),Settings.SETTINGSDATATYPES,Settings.SETTINGSTABLENAME)
