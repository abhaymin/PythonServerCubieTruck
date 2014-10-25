# -*- coding: utf-8 -*-
"""
Created on Thu Oct 23 14:35:54 2014

@author: abhaymenon
"""

import logging


class ErrorLogger():
    _loggerErr = logging.getLogger('ErrorLog')

    def __init__(self):
        self._loggerErr.setLevel(logging.ERROR)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%m/%d/%Y %I:%M:%S %p')
        fh = logging.FileHandler('errlog.log')
        fh.setLevel(logging.ERROR)
        fh.setFormatter(formatter)
        self._loggerErr.addHandler(fh)

    def errorHandle(self, errText):
        strI = "Error Occured : pyWebNoip.py : %s" % errText
        self._loggerErr.error(strI)


class InfoLogger():
    _loggerInfo = logging.getLogger('InfoLog')

    def __init__(self):
        self._loggerInfo.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%m/%d/%Y %I:%M:%S %p')
        ch = logging.FileHandler('infolog.log')
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        self._loggerInfo.addHandler(ch)

    def infoHandle(self, infoText):
        strI = "Information : pyWebNoip.py : %s" % infoText
        self._loggerInfo.info(strI)


class DebuggerPrint():
    _debugMsg = logging.getLogger('DebugLog')

    def __init__(self):
        self._debugMsg.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%m/%d/%Y %I:%M:%S %p')
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)
        ch.setFormatter(formatter)
        self._debugMsg.addHandler(ch)

    def DebugPrint(self, message):
        self._debugMsg.debug(message)

errorHandle = ErrorLogger().errorHandle
infoHandle = InfoLogger().infoHandle
DebugPrint = DebuggerPrint().DebugPrint

__all__ = ["errorHandle", "infoHandle", "DebugPrint"]
