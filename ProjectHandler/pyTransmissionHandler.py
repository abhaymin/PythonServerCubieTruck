# -*- coding: utf-8 -*-
"""
Created on Fri Oct 24 19:15:48 2014

@author: abhaymenon
"""
import sqlite3
import transmissionrpc
from transmissionrpc.utils import *

from ProjectHandler.ErrorHandler import *
from ProjectHandler.Configuration import *
from ProjectHandler.SendEmail import *


class TransimissionHandler():
    _client = None
    _torrents = None

    def __init__(self):
        self.connectTorrent()

    def connectTorrent(self):
        try:
            _tranUser = configRd.ConfigSectionMap("MyTransmission", 'tranuser')
            _tranPwd = configRd.ConfigSectionMap("MyTransmission", 'tranpwd')
            _tranServer = configRd.ConfigSectionMap("MyTransmission", 'transerver')
            _tranPort = configRd.ConfigSectionMap("MyTransmission", 'tranport')
            self._client = transmissionrpc.Client(_tranServer, port=int(_tranPort), user=_tranUser, password=_tranPwd)
            self._torrents = self._client.info()
        except Exception, e:
            errorHandle("Error in connect Torrent Server - %s" % str(e))
            raise

    def gettorrentdownloadinglist(self):
        try:
            if self._client is not None and self._torrents is not None:
                fo = open("/root/downloadlist.txt", "w")
                for k, v in self._torrents.iteritems():
                    if(v.status == 'downloading'):
                        fo.write("%s\n" % str(v.hashstring))
                fo.close()
        except IOError, e:
            errorHandle("ERROR IN GET TORRENT DOWNLOADLIST - %s" % str(e))
        except Exception, e:
            errorHandle("ERROR IN GET TORRENT DOWNLOADLIST - %s" % str(e))

    def resettorrentdownloadlist(self):
        try:
            if self._client is not None and self._torrents is not None:
                fo = open("/root/downloadlist.txt", "r")
                while True:
                    testline = fo.readline()
                    infoHandle("torrent no:"+testline.strip(" ").strip('\n'))
                    if len(testline.strip(" ")) == 0:
                        break

                    if str(self._client.get_torrent(str(testline).strip(" ").strip('\n')).status) != 'downloading':
                        self._client.start_torrent(str(testline).strip(" ").strip('\n'), True)

                fo.close()
        except IOError, e:
            errorHandle("ERROR IN RESET TORRENT DOWNLOADLIST - %s" % str(e))
        except Exception, e:
            errorHandle("ERROR IN RESET TORRENT DOWNLOADLIST - %s" % str(e))

    def stopBitTorrent(self):
        try:
            self.gettorrentdownloadinglist()
            if self._client is not None and self._torrents is not None:
                for tid, torrent in self._torrents.iteritems():
                    if(torrent.status != 'stopped'):
                        self._client.stop(torrent.hashString)
        except IOError, e:
            errorHandle("Error in stopping Torrent %s" % str(e))
        except Exception, e:
            errorHandle("Error in stopping Torrent %s" % str(e))

    def startBitTorrent(self):
        try:
            self.resettorrentdownloadinglist()
            if self._client is not None and self._torrents is not None:
                for tid, torrent in self._torrents.iteritems():
                    if(torrent.status == 'stopped'):
                        self._client.start(torrent.hashString)
        except Exception, e:
            errorHandle("Starting Torrent - %s" % str(e))

    def reannoucetorrent(self):
        try:
            if self._client is not None and self._torrents is not None:
                for k, v in self._torrents.iteritems():
                    if(v.status == 'downloading' and (format_speed(v.rateDownload)[0] != 0.0 or format_speed(v.rateUpload)[0] != 0.0)):
        #                               infoHandle('%s' % v.name)
                        self._client.reannounce_torrent(k)
                        v.update()
        except Exception, e:
            errorHandle("ERROR IN REANNOUCE TORRENT %s" % str(e))

    def checkTorrentPing(self):
        try:
            if self._client is not None and self._torrents is not None:
                for k, v in self._torrents.iteritems():
                    if format_speed(v.rateDownload)[0] != 0.0 or format_speed(v.rateUpload)[0] != 0.0:
                        return True
            return False
        except Exception, e:
            errorHandle("Checking Torrent based ping - %s" % str(e))
            return False

    def sendListOfCompletedTorrent(self):
        try:
            if self._client is not None and self._torrents is not None:
                l = []
                fo = open("/root/torrent.txt", "a+")
                valueFile = fo.read()
                for tid, torrent in torrents.iteritems():
                    if (torrent.status == 'seeding'):
                        try:
                            if(torrent.hashString not in valueFile):
                                value = ('<tr><table><tr><td>&nbsp;&nbsp;Torrent Name: </td><td>&nbsp;&nbsp;%s </td><td>&nbsp;&nbsp;HashString:</td><td>&nbsp;&nbsp;%s</td><td>&nbsp;&nbsp;</td><td>&nbsp;&nbsp;</td></tr><tr><td>&nbsp;&nbsp;Status :</td><td>&nbsp;&nbsp;%s</td><td>&nbsp;&nbsp;Progress :</td><td>&nbsp;&nbsp;%.2f%%</td><td>&nbsp;&nbsp;ETA: </td><td>&nbsp;&nbsp;NONE</td></tr></table></tr>' % (torrent.name, torrent.hashString, torrent.status, torrent.progress))
                                l.append(value)
                        except Exception, e:
                            #print "problem in torrent name";
                            errorHandle("problem in torrent Name - %s" % str(e))

                s = '\n'.join(l)
                s += '\n'
                a = ('<html><body><table>%s</table></body></html>' % s)
                if(len(l) > 0):
                    fo.write(s)
                    sendEmailTorrentDownloaded(a)

                fo.close()

        except Exception, e:
            errorHandle("some problem in find function - %s" % str(e))

    def sendListOfDownloadingTorrent(self):
        try:
            if self._client is not None and self._torrents is not None:
                l = []
                w = []
                for tid, torrent in self._torrents.iteritems():
                    if (torrent.status == 'downloading'):
                        value = ('<tr><table><tr><td>&nbsp;&nbsp;Torrent Name: </td><td>&nbsp;&nbsp;%s </td><td>&nbsp;&nbsp;HashString:</td><td>&nbsp;&nbsp;%s</td><td>&nbsp;&nbsp;</td><td>&nbsp;&nbsp;</td></tr><tr><td>&nbsp;&nbsp;Status :</td><td>&nbsp;&nbsp;%s</td><td>&nbsp;&nbsp;Progress :</td><td>&nbsp;&nbsp;%.2f%%</td><td>&nbsp;&nbsp;ETA : </td><td>&nbsp;&nbsp;NONE</td></tr></table></tr>' % (torrent.name, torrent.hashString, torrent.status, torrent.progress))
                        l.append(value)

                        w.append('%s' % torrent.hashString)

                s = '\n'.join(l)
                s += '\n'
                a = ('<html><body><table>%s</table></body></html>' % s)
                if(len(l) > 0):
                    sendEmailTorrent(a)
        #               gettorrentdownloadinglist ()
        except Exception, e:
            errorHandle("some problem in find function - %s" % str(e))


gettorrentdownloadinglist = TransimissionHandler().gettorrentdownloadinglist
resettorrentdownloadlist = TransimissionHandler().resettorrentdownloadlist
stopBitTorrent = TransimissionHandler().stopBitTorrent
startBitTorrent = TransimissionHandler().startBitTorrent
reannoucetorrent = TransimissionHandler().reannoucetorrent
checkTorrentPing = TransimissionHandler().checkTorrentPing
sendListOfDownloadingTorrent = TransimissionHandler().sendListOfDownloadingTorrent
sendListOfCompletedTorrent = TransimissionHandler().sendListOfCompletedTorrent

__all__ = ["gettorrentdownloadinglist", "resettorrentdownloadlist", "stopBitTorrent", "startBitTorrent", "reannoucetorrent", "checkTorrentPing", "sendListOfDownloadingTorrent", "sendListOfCompletedTorrent"]
