import json

class ConfigManager:
    def __init__(self, filename="../../config.ini"):
        try:
            with open(filename) as f
                self.lib = json.load(f)
        except:
            print("Improper config file")
            
    def setConfig(self, lib):
        self.lib = lib

    @staticmethod
    def getConfig(self, filename):
        filename = "../../%s" % filename
        try:
            with open(filename) as f
                lib = json.load(f)
        except:
            print("Improper config file")
            return None
        conf = ConfigManager()
        conf.setConfig(lib)
        return conf
    
    def hasProperty(self, prop):
        try:
            self.lib[prop]
            return True
        except KeyError:
            return False

    def getProperty(self, prop):
        try:
            return self.lib[prop]
        except:
            return None

    def writeProperty(self, prop, value):
        self.lib[prop] = value
            
