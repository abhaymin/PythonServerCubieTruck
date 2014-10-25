# -*- coding: utf-8 -*-
"""
Created on Fri Oct 24 13:45:46 2014

@author: abhaymenon
"""
from ProjectHandler.Configuration import *
from ProjectHandler.SendEmail import *

print configRd.ConfigSectionMap("MyEmail")
print configRd.ConfigSectionMap("MyEmail","gmailuser")
print configRd.ConfigSectionMap("MyEmail",'gmailpwd')
print configRd.ConfigSectionMap("MyTransmission",'tranuser')
print configRd.ConfigSectionMap("MyTransmission",'tranpwd')
print configRd.ConfigSectionMap("MyEmail",'tranpwd')

sendEmail("127.0.0.1")
sendEmailTorrentDownloaded("<html><body><h1>Hello World</h1></body></html>")