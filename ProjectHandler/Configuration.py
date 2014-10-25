# -*- coding: utf-8 -*-
"""
Created on Fri Oct 24 13:02:58 2014

@author: abhaymenon
"""
import ConfigParser
from ProjectHandler.ErrorHandler import DebugPrint, errorHandle


class MyConfigReader:
    _Config = ConfigParser.ConfigParser()
    _configFile = 'myConfig.ini'

    def __init__(self):
        pass

    """
        SetConfigFile is used change default configuration INI File.
    """

    def SetConfigFile(self, configFileName):
        self._configFile = configFileName

    """
        ConfigSectionMap is used change default configuration Map
        section or options under section are read from here

        Also used as method overriding pattern
    """

    def ConfigSectionMap(self, *args, **kwargs):
        # Call the function that has the same number of non-keyword arguments.
        return getattr(self, "_configSectionMap" + str(len(args)))(*args, **kwargs)

    """
        _configSectionMap1 is used change default configuration Map
        section are read from here
    """

    def _configSectionMap1(self, section):
        self._Config.read(self._configFile)
        dict1 = {}
        options = self._Config.options(section)
        for option in options:
            try:
                dict1[option] = self._Config.get(section, option)
                if dict1[option] == -1:
                    DebugPrint("skip: %s" % option)
            except Exception, exception:
                errorHandle(("exception on %s! - %s" % option, exception))
                dict1[option] = None
        return dict1

    """
        _configSectionMap2 is used change default configuration Map
        section are read from here
    """

    def _configSectionMap2(self, section, options):
        dict2 = self._configSectionMap1(section)
        if options in dict2:
            return dict2[options]

configRd = MyConfigReader()

__package__ = "ProjectHandler.Configuration"
__all__ = ["MyConfigReader", "configRd"]
