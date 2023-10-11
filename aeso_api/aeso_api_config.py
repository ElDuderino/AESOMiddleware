import configparser


class AESOAPIConfig:

    def __init__(self, config_path=None):

        # cur_dir = os.path.dirname(__file__)
        # ymmv
        # config.read(cur_dir + "\\config.ini")
        self.___config = configparser.ConfigParser()
        if config_path is None:
            self.___config.read("config.cfg")
        else:
            self.___config.read(config_path)

        self._API_URL = self.___config['AESO_API']['API_URL']
        self._API_ACCESS_TOKEN = self.___config['AESO_API']['API_ACCESS_TOKEN']

    def get_api_url(self):
        return self._API_URL

    def get_api_access_token(self):
        return self._API_ACCESS_TOKEN

    def get_value(self, value: str):
        """Get an arbitrary value from the config file
            Search all sections and return the first version of the value
        """
        ret = None
        sections = ["DEFAULT"]
        for section in self.___config.sections():
            sections.append(section)

        for section in sections:
            ret = self.___config.get(section, value)
            if ret is not None:
                break
        return ret
