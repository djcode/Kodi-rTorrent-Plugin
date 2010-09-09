# Imports
import os
import xbmc
import xbmcaddon
import xmlrpc2scgi

# Addon constants
__plugin__ = "RTorrent"
__addonID__= "plugin.program.rtorrent"
__author__ = "Daniel Jolly"
__url__ = "http://www.danieljolly.com"
__credits__ = "Team XBMC for amazing XBMC! Jari \"Rakshasa\" Sundell, the developer of the fantastic rTorrent"
__version__ = "0.10.0"
__date__ = "08/01/2010"

#Set a variable for Addon info and language strings
__addon__ = xbmcaddon.Addon( __addonID__ )
__lang__ = __addon__.getLocalizedString

# Connection constants
# Check to see if addon is set to socket or port mode
if int(__addon__.getSetting('use_socket')) == 1:
	__connection__ = 'scgi://'+__addon__.getSetting('domain_socket')
else:
	__connection__ = 'scgi://'+str(__addon__.getSetting('scgi_server'))+':'+str(__addon__.getSetting('scgi_port'))

rtc = xmlrpc2scgi.RTorrentXMLRPCClient(__connection__)

# Directory containing status icons for torrents
__icondir__ = xbmc.translatePath(os.path.join(os.getcwd(),'resources','icons'))