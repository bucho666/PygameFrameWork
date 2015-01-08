# -*- coding: utf-8 -*-
import ConfigParser
class ConfigFile(object):
    def __init__(self, filename):
        self._filename = filename
        self._config = ConfigParser.SafeConfigParser()

    def set(self, section, option, value):
        if not self._config.has_section(section):
            self._config.add_section(section)
        self._config.set(section, option, value)
        self._save()

    def load(self):
        self._config.read(self._filename)
        return self

    def items(self, section):
        if not self._config.has_section(section):
            return []
        return self._config.items(section)

    def _save(self):
        fp = open(self._filename, 'w')
        self._config.write(fp)
        fp.close()
