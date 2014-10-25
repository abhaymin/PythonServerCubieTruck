# -*- coding: utf-8 -*-
"""
Created on Thu Oct 23 14:35:54 2014

@author: abhaymenon
"""

import time
import subprocess
import datetime
import ping
import sys
import socket


class NetworkIP():

        def __init__(self):
                pass

        def ifLinkBeatIP(netwrk):
                stat = 'ifconfig %s | grep -e "inet addr"' % netwrk
                p = subprocess.Popen(stat, shell=True, stdout=subprocess.PIPE)
                finddata = 'inet addr'
                for line in p.readlines():
                        if finddata in line:
                                return True
                return False

        def ifLinkBeat(self, netwrk):
                stat = 'ifplugstatus | grep -e "%s" | awk -F": " "{ print $2 }"' % netwrk
                p = subprocess.Popen(stat, shell=True, stdout=subprocess.PIPE)
                data = p.communicate()
                if data == "link beat detected":
                        return True
                return False

        def ifLinkUp(self, netwrk):
                arg = 'ifup %s' % netwrk
                os.system('%s' % arg)

        def ifLinkDown(self, netwrk):
                arg = 'ifdown %s' % netwrk
                os.system('%s' % arg)

        def checkNetLink(self, netwrk):
                if ifLinkBeat(netwrk) is False or ifLinkBeatIP(netwrk) is False:
                        ifLinkDown(netwrk)
                        ifLinkUp(netwrk)


checkNetLink = NetworkIP().checkNetLink
ifLinkDown = NetworkIP().ifLinkDown
ifLinkUp = NetworkIP().ifLinkUp
