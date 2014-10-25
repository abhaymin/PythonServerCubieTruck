# -*- coding: utf-8 -*-
"""
Created on Thu Oct 23 14:35:03 2014

@author: abhaymenon
"""

import urllib2
import base64
import time
import subprocess
import os
import datetime
import sys
import socket
import ping
import re
import httplib

from ProjectHandler.ErrorHandler import *
from ProjectHandler.Configuration import *
from ProjectHandler.SendEmail import *


class IPAddressHandler():

        def __init__(self):
                pass

        def getIPAddr(self, func):
                try:
                        arg = 'ifconfig ppp0 | sed -n "/inet /{s/.*addr://;s/ .*//;p}"'
                        p = subprocess.Popen(arg, shell=True, stdout=subprocess.PIPE)
                        data = p.communicate()
                        split_data = data[0].split()
                        ipaddr = split_data[0]
                        DebugPrint("%s" % ipaddr)
                        return ipaddr
                except Exception, e:
                        errorHandle("getIPAddr(%s) - Unable to processs - %s - %s" % func, func, str(e))
                        return ''

        def updateIptoFile(self, ipaddr):
                try:
                        f = open('/root/currentip', 'w')
                        f.write(ipaddr)
                        f.close()
                except Exception, e:
                        errorHandle("noipUpdate() - unable to update ip - %s" % str(e))

        def getOldip(self):
                try:
                        f = open('/root/currentip', 'r')
                        ipaddr = f.read()
                        f.close()
                        return ipaddr
                except Exception, e:
                        errorHandle("getOldip() - unable to read file /root/currentip %s" % str(e))
                        return ''

        def checkOldIpToNewIp(self):
                infoHandle("Check Old IP to New IP - Starting")
                cur_ipaddr = self.getIPAddr("checkOldIpToNewIp")
                old_ipaddr = self.getOldip()
                if cur_ipaddr != old_ipaddr:
                        infoHandle("Check Old IP to New IP - Change Found!!")
                        try:
                                infoHandle("Check Old IP to New IP - start the ip update process")
                                if noipUpdate(cur_ipaddr) is False:
                                        noipUpdate('')
                                infoHandle("Check Old IP to New IP - ending the ip update process")
                        except Exception, e:
                                errorHandle("checkOldIpToNewIp() - Unable to update the IP to noip - %s" % str(e))
                infoHandle("Check Old IP to New IP - Ending")

        def getIPAddrRemote(self, func):
                try:
                        username = configRd.ConfigSectionMap("MyRemoteService", "username")
                        password = configRd.ConfigSectionMap("MyRemoteService", "password")
                        remoteip = configRd.ConfigSectionMap("MyRemoteService", "remoteip")
                        arg = 'sshpass -p %s ssh %s@%s  ifconfig ppp0 | sed -n "/inet /{s/.*addr://;s/ .*//;p}"' % password, username, remoteip
                        p = subprocess.Popen(arg, shell=True, stdout=subprocess.PIPE)
                        data = p.communicate()
                        split_data = data[0].split()
                        ipaddr = split_data[0]
                        DebugPrint("%s" % ipaddr)
                        return ipaddr
                except Exception, e:
                        errorHandle("getIPAddrRemote() - Unable to processs - " + func + " - " + str(e))
                        return ''

        def checkOldIpToNewIpRemote(self):
                infoHandle("Check Old IP to New IP - Starting")

                cur_ipaddr = getIPAddrRemote("checkOldIpToNewIp")
                old_ipaddr = getOldip()
                if cur_ipaddr != old_ipaddr:
                        infoHandle("Check Old IP to New IP - Change Found!!")
                        try:
                                infoHandle("Check Old IP to New IP - start the ip update process")
                                if self.noipUpdate(cur_ipaddr) is False:
                                        self.noipUpdate('')
                                infoHandle("Check Old IP to New IP - ending the ip update process")
                        except Exception, e:
                                errorHandle("checkOldIpToNewIp() - Unable to update the IP to noip - %s" % str(e))

                infoHandle("Check Old IP to New IP - Ending")

        def noipUpdate(self, ipaddr):
                try:
                        infoHandle("Update NoIP.com - Starting")
                        noipUpdateIPUrl = configRd.ConfigSectionMap("MyNoIP", "noipupdateipurl")
                        noipHostName = configRd.ConfigSectionMap("MyNoIP", "noiphostname")
                        noipUserName = configRd.ConfigSectionMap("MyNoIP", "noipusername")
                        noipPassword = configRd.ConfigSectionMap("MyNoIP", "noippassword")
                        noipUserAgentString = configRd.ConfigSectionMap("MyNoIP", "noipuseragentstring")
                        noipWaitTimeIP = configRd.ConfigSectionMap("MyNoIP", "noipwaittimeip")
                        noipWaitTimeNoIP = configRd.ConfigSectionMap("MyNoIP", "noipwaittimenoip")
                        noipbase64 = "%s:%s" % noipUserName, noipPassword

                        if ipaddr != '':
                                url = noipUpdateIPUrl % ipaddr, noipHostName
                        else:
                                url = noipUpdateIPUrl % '', noipHostName

                        request = urllib2.Request(url)
                        base64string = base64.encodestring(noipbase64).replace('\n', '')
                        request.add_header("Authorization", "Basic %s" % base64string)
                        request.add_header("User-Agent", noipUserAgentString)

                        if ipaddr != '':
                                response = urllib2.urlopen(request, timeout=int(noipWaitTimeIP))
                        else:
                                response = urllib2.urlopen(request, timeout=int(noipWaitTimeNoIP))

                        data = response.read()
                        if ipaddr != '':
                                if data.find(ipaddr) != -1:
                                        self.updateIptoFile(ipaddr)
                                        sendEmailIP(ipaddr)
                                        time.sleep(15)
                        else:
                                addressgrep = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
                                ipmatch = addressgrep.search(str(data))
                                if ipmatch is not None:
                                        ipaddr = ipmatch.group()
                                        self.updateIptoFile(ipaddr)
                                        sendEmailIP(ipaddr)
                                        time.sleep(15)
                        infoHandle("Update NoIP.com - %s - Ending" % data)
                        return True
                except Exception, e:
                        errorHandle("noipUpdate() - unable to update ip : %s" % str(e))
                        if ipaddr != '':
                                self.updateIptoFile(ipaddr)
                                sendEmailIPFailed(ipaddr)
                                time.sleep(10)
                        return False

checkOldIpToNewIp = IPAddressHandler().checkOldIpToNewIp
checkOldIpToNewIpRemote = IPAddressHandler().checkOldIpToNewIpRemote
getIPAddr = IPAddressHandler().getIPAddr
getIPAddrRemote = IPAddressHandler().getIPAddrRemote
getOldip = IPAddressHandler().getOldip
noipUpdate = IPAddressHandler().noipUpdate
updateIptoFile = IPAddressHandler().updateIptoFile

__package__ = "NetworkHandler.IPAddressHandler"
__all__ = ["checkOldIpToNewIp", "checkOldIpToNewIpRemote", "getIPAddr", "getIPAddrRemote", "getOldip", "noipUpdate", "updateIptoFile"]
