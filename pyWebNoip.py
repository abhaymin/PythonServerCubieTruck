#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 23 14:35:54 2014

@author: abhaymenon
"""

from daemon import runner
import urllib2
import base64
import time
import subprocess
import os
import datetime
import ping
import sys
import socket
import ping
import re
import httplib

from ProjectHandler.ErrorHandler import *
from ProjectHandler.Configuration import *
from ProjectHandler.SendEmail import *
from ProjectHandler.pyTransmissionHandler import *
from NetworkHandler.NetworkHandler import *
from NetworkHandler.IPAddressHandler import *

count = 0
xount = 0
reusb = 0
resetppd = 0
resetwv = 0
newIp = ""
oldIp = ""


def checkDirLog(filename):
        p = os.popen('ls /var/log')
        for line in p.readlines():
                if filename in line:
                        return True
        return False


def checkDirRun(filename):
        p = os.popen('ls /var/run')
        for line in p.readlines():
                if filename in line:
                        return True
        return False


def checkDev(filename):
        p = os.popen('lsusb')
        for line in p.readlines():
                if filename in line:
                        return True
        return False


def makeDir(filename):
        os.system(filename)


def checkServiceStatus(filename):
        p = os.popen('ps aux')
        for line in p.readlines():
                if filename in line:
                        return True
        return False


def resetStoppedService(filename):
        if checkServiceStatus(filename) is False:
                infoHandle('Restarting Stopped Service - %s' % filename)
                os.system('service %s start' % filename)


def resetSambaService():
        if checkServiceStatus('smbd') is False:
                os.system('service samba restart')
#               os.system('service smbd restart')
#               os.system('service nmbd restart')


def checkWvDial():
        infoHandle("Check WvDIAL - Starting")

        cur_ipaddr = getIPAddr("checkWvDial")
        if (cur_ipaddr == ''):
                if checkServiceStatus('wvdial') is False:
                        os.system('killall wvdial')
                        resetWVdialService()
                        time.sleep(40)
        infoHandle("Check WvDIAL - Ending")


def checkDeviceFileExists(filename):
        p = os.popen('ls /dev')
        for line in p.readlines():
                if filename in line:
                        return True
        return False


def resetUSB():
        infoHandle("reseting USB - Starting")

        try:
                if checkServiceStatus('wvdial') is False:
                        os.system('echo 0 > /sys/bus/usb/devices/1-1.2/remove')
                        os.system('echo 0 > /sys/bus/usb/devices/1-1/authorized')
                        time.sleep(10)
                        os.system('echo 1 > /sys/bus/usb/devices/1-1/authorized')
                        os.system('/usr/local/bin/usb')
        except Exception, e:
                errorHandle("resetUSB() - Unable to Reset USB devices - %s" % str(e))
        infoHandle("reseting USB - Ending")


def resetWVdialService():
        global reusb
        infoHandle("reseting WvDIAL - Starting")

        try:
                if checkServiceStatus('wvdial') is False:
                        #if reusb > 10 :
                        #       #resetUSB();
                        #       reusb = 0;
                        #else:
                        #       reusb = reusb + 1;
                        #time.sleep(10);
                        #os.system('usb');
                        #makeDir('/var/log/umtskeeper')
                        #makeDir('/var/run/umtskeeper')
                        #time.sleep(10);

                        if checkDeviceFileExists("ttyUSB0") is True:
#                               if checkDev("E398") == True :
                                #os.system('wvdial &');
                                os.system('service ppp-client start')
#                                       os.system('/root/utmskeeper/umtskeeper --conf /etc/umtskeeper.conf &');
                                infoHandle("reseting WvDIAL - Dialed Out")
                                time.sleep(120)

#                               if checkDev("Hauwei") == True :
#                                       os.system('wvdial mtnl3g &');
#                                       os.system('/root/utmskeeper/umtskeeper --conf /etc/umtskeeper.conf &');
#                                       infoHandle("reseting WvDIAL - Dialed Out");
#                                       time.sleep(120);
#
                        if checkDeviceFileExists("ttyACM0") is True:
                                #os.system('wvdial mtnl3gZ &')
                                os.system('wvdial &')
#                               os.system('/root/utmskeeper/umtskeeper --conf /etc/umtskeeper.zte.conf &');
                                infoHandle("reseting WvDIAL - ZTE - Dialed Out")
                                time.sleep(120)

        except Exception, e:
                errorHandle("resetWVdialService() - Unable to Reset WvDial and USB.sh - %s" % str(e))
        infoHandle("reseting WvDIAL - Ending")


def checkMountDrive(mount):
        infoHandle("Check Mount Drive - %s" % mount)

        try:
                p = os.popen('mount')
                for line in p.readlines():
                        if mount in line:
                                return True
                return False
        except Exception, e:
                errorHandle("Check Mount Drive - %s" % str(e))
                return False


def checkFailMount(mount):
        infoHandle("Check Failed Mount - %s" % mount)

        try:
                p, d, f = os.walk(mount).next()
                countOfDir = len(d)
                if countOfDir > 1:
                        return True
                return False
        except Exception, e:
                errorHandle("Check Failed Mount Drive - %s" % str(e))
                return False


def stopAllServiceHDD():
        infoHandle("Stop all Service for HDD Mount")

        try:
#               os.system('service smbd stop')
#               os.system('service nmbd stop')
                os.system('service samba stop')

                os.system('service webmin stop')
                os.system('service minidlna stop')
                os.system('service mediatomb stop')
                gettorrentdownloadinglist()
                os.system('service transmission-daemon stop')
        except Exception, e:
                errorHandle("Failed to stop all service - %s" % str(e))


def startAllServiceHDD():
        infoHandle("Starting all Service for HDD Mount")

        try:
#               os.system('service smbd start')
#               os.system('service nmbd start')
                os.system('service samba start')
                os.system('service webmin start')
                os.system('service minidlna start')
                os.system('service mediatomb start')
                os.system('service transmission-daemon start')
                resettorrentdownloadinglist()
        except Exception, e:
                errorHandle("Failed to start all service  - %s" % str(e))


def mountDrive(label, mount, type, option):
        global xount
        infoHandle("Mounting Drive - Starting")

        try:
                if checkFailMount(mount) is False:
                        stopAllServiceHDD()
                        subprocess.Popen(["umount", mount])
                else:
                        return True
        except Exception, e:
                sendEmail("Failed Mount Drive -- inner error -- error checkFailMount :: " + mount + " - " + str(e))
                errorHandle("Failed Mount Drive -- inner error -- error checkFailMount :: " + mount + " - " + str(e))
                return False

        try:
                if checkMountDrive(mount) is False:
                        subprocess.Popen(["mount", "-t", type, label, mount, "-o", option])
                        if checkMountDrive(mount) is True:
                                startAllServiceHDD()
                                xount = 0
                        else:
                                xount = xount + 1
                                infoHandle("Mounting Drive - Failure Count - %d" % xount)
                                return False
                else:
                        return True

        except Exception, e:
                sendEmail("Failed Mount Drive -- inner error -- checkMountDrive :: " + mount + " - " + str(e))
                errorHandle("Failed Mount Drive -- inner error -- checkMountDrive :: " + mount + " - " + str(e))
                return False

        if xount > 30:
                sendEmail("Failed to mount Drive 30 times -- hence powerdown")
                return False
#               os.system("poweroff")
        infoHandle("Mounting Drive - Ending")
        return True


def sReboot():
        sendEmail("System Rebooting")
        os.system("reboot")


def checkPing(addr, sec=1000):
        infoHandle("Checking Ping for %s" % addr)

        try:
                delay = ping.do_one(addr, sec, 64)

                if delay is None:
                        return False
                return True
        except Exception, e:
                errorHandle("check ping - %s" % str(e))
                return False


def resetWvDial():
        if checkTorrentPing() is False:
                if checkPing('8.8.8.8', 20) is False:
                        infoHandle("Reset WvDial failed in Ping Back Test")
                        if checkServiceStatus('wvdial') is True:
                                os.system('killall wvdial')
                        time.sleep(10)
                        resetWVdialService()
                        time.sleep(10)
                        os.system('cp /etc/resolv.conf /etc/resolv.conf.bak')
                        #os.system('cp /etc/resolv.conf.up /etc/resolv.conf')


def resetEth0Network():
        try:
                if checkPing('192.168.1.1') is False:
                        ifLinkDown('eth0')
                        ifLinkUp('eth0')
                        time.sleep(5)
        except:
                errorHandle("some problem in link - eth0")


def resetWifi():
        if checkTorrentPing() is False:
                if checkPing('192.168.12.1', 20) is False:
                        infoHandle("Reset Wifi failed in Ping Back Test")
                        os.system('ifdown wlan0')
                        time.sleep(5)
                        os.system('ifup wlan0')
                        time.sleep(20)


def resetRemoteW():
        if checkTorrentPing() is False:
                if checkPing('8.8.8.8', 20) is False:
                        infoHandle("Reset 8.8.8.8 failed in Ping Back Test")
                        username = configRd.ConfigSectionMap("MyRemoteService", "username")
                        password = configRd.ConfigSectionMap("MyRemoteService", "password")
                        remoteip = configRd.ConfigSectionMap("MyRemoteService", "remoteip")
                        arg = 'sshpass -p %s ssh %s@%s  killall pppd' % password, username, remoteip
                        os.system(arg)
                        time.sleep(20)


def resetW():
        if checkTorrentPing() is False:
                if checkPing('8.8.8.8', 20) is False:
                        infoHandle("Reset 8.8.8.8 failed in Ping Back Test")
                        os.system('killall wvdial')
                        time.sleep(10)
                        os.system('service ppp-client start')
                        time.sleep(20)
                        checkOldIpToNewIp()


def startEvent():
        global count
        global xount
        global resetwv
        global resetppd
        DebugPrint("Start of Python based NoIP script")
        infoHandle("Start of Python based NoIP script")

        if True:
                try:
#                       mountDrive('UUID="00012F09000AD9EA"','/mnt/Elements','ntfs-3g','rw,exec,user,defaults')
#                       mountDrive('UUID="6E86CB0E51799059"','/mnt/Freecom','ntfs-3g','rw,exec,user,defaults')
                        mountDrive('UUID="01CEB6B7F7446C50"', '/mnt/Elements', 'ntfs-3g', 'rw,exec,user,defaults')
                except Exception, e:
                        errorHandle("Failed Event Mount -- outer error - %s" % str(e))

                try:
                        resetW()
                        if resetwv > 5:
                                reannoucetorrent()
                                checkOldIpToNewIp()
                                resetwv = 0
                        else:
                                resetwv = resetwv + 1
                except Exception, e:
                        errorHandle("startEvent() - resetWifi = Failed Event : Wifi check - %s" % str(e))

                try:
                        if checkMountDrive('/mnt/Elements') is True:
                                resetStoppedService('transmission-daemon')
                                resettorrentdownloadinglist()
                except Exception, e:
                        print "Failed Event - Transmission - %s " % str(e)
                        errorHandle("Failed Event - Transmission - %s" % str(e))

                try:
                        if checkMountDrive('/mnt/Elements') is True:
                                startBitTorrent()
                except Exception, e:
                        print "Failed Event : Transmission-Daemon"
                        errorHandle("Failed Event : Transmission-Daemon - %s" % str(e))

                try:
                        resetStoppedService('webmin')
                except Exception, e:
                        print "Failed Event - webmin"
                        errorHandle("Failed Event - webmin - %s" % str(e))

                try:
                        if checkMountDrive('/mnt/Elements') is True:
                                resetStoppedService('mediatomb')
                except Exception, e:
                        print "Failed Event - mediatomb"
                        errorHandle("Failed Event - mediatomb - %s" % str(e))

                try:
                        if checkMountDrive('/mnt/Elements') is True:
                                resetStoppedService('minidlna')
                except Exception, e:
                        print "Failed Event - minidlna"
                        errorHandle("Failed Event - minidlna - %s" % str(e))

                try:
                        if checkMountDrive('/mnt/Elements') is True:
                                resetStoppedService('apache2')
                except Exception, e:
                        print "Failed Event - apache2"
                        errorHandle("Failed Event - apache2 - %s" % str(e))

                try:
                        if checkMountDrive('/mnt/Elements') is True:
                                resetSambaService()
                except Exception, e:
                        print "Failed Event - Samba"
                        errorHandle("Failed Event - Samba - %s" % str(e))

                try:
                        if checkMountDrive('/mnt/Elements') is True:
                                sendListOfCompletedTorrent()
                except Exception, e:
                        print "Failed Event : Send List"
                        errorHandle("Failed Event : Send List - %s" % str(e))

                try:
                        if count > 29:
                                sendListOfDownloadingTorrent()
                                count = 0
                except Exception, e:
                        errorHandle("Failed Event : Send List - %s" % str(e))

                count = count + 1

                time.sleep(60)


def checkalreadyexist():
        try:
                p = os.popen('ls /var/run')
                for line in p.readlines():
                        if 'noips.pid' in line:
                                return True
                return False
        except:
                return False


os.system('touch /root/currentip')


class MyDaemon():
        def __init__(self):
                self.stdin_path = '/dev/null'
                self.stdout_path = '/var/log/noips.info.log'
                self.stderr_path = '/var/log/noips.err.log'
                self.pidfile_path = '/var/run/noips.pid'
                self.pidfile_timeout = 5

        def run(self):
                if checkalreadyexist() is False:
                        sendEmail("..System has Started..")

                while True:
                        startEvent()
                        time.sleep(10)

if __name__ == "__main__":
        daemon = MyDaemon()
        daemon_runner = runner.DaemonRunner(daemon)
        daemon_runner.do_action()
