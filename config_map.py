import ConfigParser
Config = ConfigParser.ConfigParser()
Config.read("device.config")


class ConfigMap(object):
    def config_section_map(self, section):
        dict1 = {}
        options = Config.options(section)
        for option in options:
            try:
                dict1[option] = Config.get(section, option)
                if dict1[option] == -1:
                    print("skip: %s" % option)
            except:
                print("exception on %s!" % option)
                dict1[option] = None
        return dict1

    def write_power_profile(self, powerlimit, priority):
        cfgfile = open("device.config", 'w')
        if (not Config.has_section('userprofile')):
            Config.add_section('userprofile')
        Config.set('userprofile', 'powerlimit', powerlimit)
        Config.set('userprofile', 'priority', priority)
        Config.write(cfgfile)
        cfgfile.close()

    def write_config(self, section, key, value):
        cfgfile = open("device.config", 'w')
        if (not Config.has_section(section)):
            Config.add_section(section)
        Config.set(section, key, value)
        Config.write(cfgfile)
        cfgfile.close()
