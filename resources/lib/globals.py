'''Global stuff across the plugin'''
# Imports
import os
import sys
import xmlrpc.client
from urllib.parse import urlparse
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import xbmcvfs
from . import rtorrent_xmlrpc

# Addon constants
__plugin__ = "RTorrent"
__addonID__= "plugin.program.rtorrent"
__author__ = "Daniel Jolly"
__url__ = "http://www.danieljolly.com"
__credits__ = "See README"
__version__ = "19.21.9"
__date__ = "09/09/2021"

#Set a variable for Addon info and language strings
__addon__ = xbmcaddon.Addon( __addonID__ )
__setting__ = __addon__.getSettingString
__lang__ = __addon__.getLocalizedString
__cwd__ = __addon__.getAddonInfo('path')

#Set plugin fanart
xbmcplugin.setPluginFanart(int(sys.argv[1]), os.path.join(__cwd__,'resources','fanart.jpg'))

# Connection constants
# Check to see if addon is set to socket or port mode

def plugin_exit():
    ''' Try to leave the plugin as cleanly as possible. '''
    xbmc.executebuiltin('Container.Update(path,replace)')

# Directory containing status icons for torrents
__icondir__ = xbmcvfs.translatePath(os.path.join(__cwd__,'resources','icons'))
