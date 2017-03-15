from configparser import ConfigParser

class Config():
    def __init__(self, path):
        self.config = ConfigParser()
        self.config.read(path)

    def getMap(self, section):
        config_dict = {}
        options = self.config.options(section)
        for option in options:
            try:
                config_dict[option] = self.config.get(section, option)
                if config_dict[option] == -1:
                    DebugPrint("skip: %s" % option)
            except:
                print("exception on %s!" % option)
                config_dict[option] = None
        return config_dict

    def get(self, section, option):
        return self.config.get(section, option)
