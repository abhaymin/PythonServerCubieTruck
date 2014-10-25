# -*- coding: utf-8 -*-
"""
Created on Thu Oct 23 14:35:54 2014

@author: abhaymenon
"""
import smtplib, datetime, sys
from email.mime.text import MIMEText
from ProjectHandler.Configuration import *
from ProjectHandler.ErrorHandler import infoHandle, errorHandle

def _sendEmails(_Subject, _Body, _To, _MailType='Text'):
    try:
        # Change to your own account information
        infoHandle("Send eMail Master Function - Starting")

        gmailUser = configRd.ConfigSectionMap("MyEmail", "gmailuser")
        gmailPwd = configRd.ConfigSectionMap("MyEmail", "gmailpwd")
        _port = configRd.ConfigSectionMap("MyEmail", "port")
        _smtpserver = configRd.ConfigSectionMap("MyEmail", "smtpserver")
        _From = gmailUser
        
        smtpserver = smtplib.SMTP(_smtpserver, _port)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo()
        smtpserver.login(gmailUser, gmailPwd)
        # Very Linux Specific

        if _MailType != 'Text':
            msg = MIMEText(_Body, _MailType)
            msg['Subject'] = str(_Subject)
            msg['From'] = str(_From)
            msg['To'] = str(_To)
            msg['Content-Type'] = "text/html; charset=utf-8"
        else:
            msg = MIMEText(_Body)
            msg['Subject'] = str(_Subject)
            msg['From'] = str(_From)
            msg['To'] = str(_To)
            
        smtpserver.sendmail(str(_From), [str(_To)], msg.as_string())
        smtpserver.quit()
        infoHandle("Send eMail Master Function - Ending")
    except smtplib.SMTPException as e:
        errorHandle("_sendEmail : Unable send mail - %s" % str(e))
    except:
        errorHandle("_sendEmail : Unable send mail - Unknown error" % sys.exc_info()[0])
        raise

def sendEmailIP(ipaddr):
    try:
        # Change to your own account information
        infoHandle("Send eMail IP - Starting")
        _To = configRd.ConfigSectionMap("MyEmail", "gmailuser")
        # Very Linux Specific
        _Body = 'Current CubieServer %s' %  ipaddr
        _Subject = 'CubieServer IP - %s' % datetime.datetime.now().strftime("%b %d %Y %H:%M:%S")
        _sendEmails(_Subject, _Body, _To)
        infoHandle("Send eMail IP - Ending")
    except Exception as e:
        errorHandle("sendEmailIP : Unable send mail - %s" % str(e))

def sendEmailIPFailed(ipaddr):
    try:
        # Change to your own account information
        infoHandle("Send eMail IP - Starting")
        _To = configRd.ConfigSectionMap("MyEmail", "gmailuser")
        # Very Linux Specific
        _Body = 'Current CubieServer %s' %  ipaddr
        _Subject = 'CubieServer IP - %s - Failed to Update' % datetime.datetime.now().strftime("%b %d %Y %H:%M:%S")
        _sendEmails(_Subject, _Body, _To)
        infoHandle("Send eMail IP - Ending")
    except Exception as e:
        errorHandle("sendEmailIP : Unable send mail - %s" % str(e))

def sendEmail(ipaddr):
    try:
        # Change to your own account information
        infoHandle("Send eMail - Starting")
        _To = configRd.ConfigSectionMap("MyEmail", "gmailuser")
        # Very Linux Specific
        _Body = 'My CubiServer is %s' %  ipaddr
        _Subject = 'CubiServer System Message %s' % datetime.datetime.now().strftime('%b %d %Y %H:%M:%S')
        _sendEmails(_Subject, _Body, _To)
        infoHandle("Send eMail - Ending")
    except Exception as e:
        errorHandle("sendEmail : Unable send mail - %s" % str(e))

def sendEmailTorrentDownloaded(message):
    try:
        # Change to your own account information
        infoHandle("Sending Email for Torrent downloaded - Starting")
        _To = configRd.ConfigSectionMap("MyEmail", "gmailuser")
        # Very Linux Specific
        _Body = 'Torrent \n %s ' % message
        _Subject = 'CubieServer Torrent Downloaded %s' % datetime.datetime.now().strftime('%b %d %Y %H:%M:%S')
        _MailType = 'html'
        _sendEmails(_Subject, _Body, _To, _MailType)
        infoHandle("Sending Email for Torrent downloaded - Ending")
    except Exception as e:
        errorHandle("sendEmailTorrentDownloaded : Unable send mail %s" % str(e))

def sendEmailTorrent(message):
    try:
        # Change to your own account information
        infoHandle("Sending Email for Torrent downloads - starting")
        _To = configRd.ConfigSectionMap("MyEmail", "gmailuser")
        # Very Linux Specific
        _Body = 'Torrent \n %s ' % message
        _Subject = 'CubieServer Torrent Downloading %s' % datetime.datetime.now().strftime('%b %d %Y %H:%M:%S')
        _MailType = 'html'
        _sendEmails(_Subject, _Body, _To, _MailType)
        infoHandle("Sending Email for Torrent downloads - Ending")
    except Exception as e:
        errorHandle("sendEmailTorrent : Unable send mail %s" % str(e))

__all__ = ["sendEmailTorrent", "sendEmailTorrentDownloaded", "sendEmail", "sendEmailIPFailed", "sendEmailIP"]