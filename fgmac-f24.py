#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  fgmac-f24.py
#
#  Copyright 2016 youcef sourani <youcef.m.sourani@gmail.com>
#
#  www.arfedora.blogspot.com
#
#  www.arfedora.com
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

import os
import subprocess
import platform
import sys
import time





############################################################################################
def init_check():

    if os.getuid()==0:
        sys.exit("Run Script Without Root Permissions.")

    if platform.linux_distribution()[0]!="Fedora" and platform.linux_distribution()[1]!="24":
        sys.exit("Fedora 24 Not Found.")


    if not sys.version.startswith("3"):
        sys.exit("Use Python 3 Try run python3 fmac.py")


    if os.getenv("XDG_CURRENT_DESKTOP")!="GNOME" :
        sys.exit("Your Desktop Is Not gnome shell")

init_check()
#############################################################################################





#############################################################################################
home=os.getenv("HOME")
dirname=os.path.abspath(os.path.dirname(__file__))


def get_all_extensions():
	result=[]
	if os.path.isdir("%s/.local/share/gnome-shell/extensions"%home):
		for filee in os.listdir("%s/.local/share/gnome-shell/extensions"%home):
			if filee not in result:
				result.append(filee)

	if os.path.isdir("/usr/local/share/gnome-shell/extensions"):
		for filee in os.listdir("/usr/local/share/gnome-shell/extensions"):
			if filee not in result:
				result.append(filee)

	for filee in os.listdir("/usr/share/gnome-shell/extensions"):
		if filee not in result:
			result.append(filee)

	return result

old_extension=get_all_extensions()
############################################################################################





############################################################################################


extensions_to_enable=["places-menu@gnome-shell-extensions.gcampax.github.com",\
                      "apps-menu@gnome-shell-extensions.gcampax.github.com",\
                      "launch-new-instance@gnome-shell-extensions.gcampax.github.com",\
                      "activities-config@nls1729","favorites@cvine.org","hide-dash@xenatt.github.com",\
                      "Move_Clock@rmy.pobox.com","CoverflowAltTab@palatis.blogspot.com",\
                      "clipboard-indicator@tudmotu.com",\
                      "drive-menu@gnome-shell-extensions.gcampax.github.com",\
                      "user-theme@gnome-shell-extensions.gcampax.github.com"]


gsettings=["gsettings set org.gnome.desktop.background show-desktop-icons false",\
           "gsettings set org.gnome.desktop.background  picture-uri \
           'file://%s/Pictures/gnome/Dark_Ivy.jpg' "%home,\
           "gsettings set org.gnome.desktop.screensaver picture-uri \
           'file://%s/Pictures/gnome/Blinds.jpg' "%home,\
           "gsettings set org.gnome.desktop.interface icon-theme 'Paper' ",\
           "gsettings set org.gnome.shell.extensions.user-theme name 'Gmac-Shell' ",\
           "gsettings set org.gnome.nautilus.preferences sort-directories-first true",\
           "gsettings set org.gnome.nautilus.preferences executable-text-activation ask",\
           "gsettings set org.gnome.desktop.peripherals.touchpad tap-to-click true",\
           "gsettings set org.gnome.desktop.interface gtk-theme  OSX-Arc-White",\
           "gsettings set org.gnome.desktop.interface enable-animations true",\
           "gsettings set org.gnome.desktop.wm.preferences button-layout ':minimize,maximize,close' ",\
           "gsettings set org.gnome.nautilus.preferences always-use-location-entry false",\
           "gsettings set org.gnome.desktop.interface cursor-theme 'Gmac-Cursor' ",\
           "gsettings set org.gnome.Terminal.Legacy.Settings theme-variant light",\
           "gsettings set org.gnome.Terminal.Legacy.Settings default-show-menubar false"]


dconf=["dconf reset -f  /net/launchpad/plank/",\
					"dconf write   /net/launchpad/plank/docks/dock1/theme \"\'UbuntuOSXMavesemite\'\"",\
					"dconf reset -f /org/gnome/shell/extensions/activities-config/",\
					"dconf reset -f /org/gnome/shell/extensions/coverflowalttab/",\
					"dconf reset -f /org/gnome/shell/extensions/favorites/",\
					"dconf write /org/gnome/shell/extensions/activities-config/transparent-panel 0", \
					"dconf write /org/gnome/shell/extensions/activities-config/activities-config-button-no-text false",\
					"dconf write /org/gnome/shell/extensions/activities-config/activities-icon-padding 5",\
					"dconf write /org/gnome/shell/extensions/activities-config/activities-config-button-no-icon false",\
					"dconf write /org/gnome/shell/extensions/activities-config/activities-config-button-icon-path \"\'%s/.icons/logo-top.png\'\""%home,\
					"dconf write /org/gnome/shell/extensions/activities-config/enable-conflict-detection true",\
					"dconf write /org/gnome/shell/extensions/activities-config/activities-config-hot-corner-delay 0",\
					"dconf write /org/gnome/shell/extensions/activities-config/maximized-window-effect 0",\
					"dconf write /org/gnome/shell/extensions/activities-config/panel-hide-app-menu-button-icon false",\
					"dconf write /org/gnome/shell/extensions/activities-config/activities-text-padding 0",\
					"dconf write /org/gnome/shell/extensions/activities-config/panel-background-color-hex-rgb \"\'#ffffff\'\"",\
					"dconf write /org/gnome/shell/extensions/activities-config/panel-hide-rounded-corners false",\
					"dconf write /org/gnome/shell/extensions/activities-config/activities-config-button-text \"\'Dashbord\'\"",\
					"dconf write /org/gnome/shell/extensions/activities-config/activities-config-hot-corner false",\
					"dconf write /org/gnome/shell/extensions/activities-config/first-enable false",\
					"dconf write /org/gnome/shell/extensions/activities-config/activities-config-button-removed \"false\"",\
					"dconf write /org/gnome/shell/extensions/favorites/icon false",\
					"dconf write /org/gnome/shell/extensions/favorites/position 2"]





#########################################################################################################



def make_folders():
    folders=["%s/.icons"%home,"%s/.themes"%home,"%s/.local/share/gnome-shell/extensions"%home,\
             "%s/.config/autostart"%home,"%s/.local/share/plank/themes"%home,"%s/.config/plank/dock1/"%home]
    for folder in folders:
        os.makedirs(folder,exist_ok=True)

make_folders()



def install_packs():
    check=subprocess.call("sudo dnf install  -y -C --best  gnome-shell-extension-user-theme \
                    gnome-shell-extension-places-menu dconf plymouth-plugin-script  GConf2 gnome-tweak-tool \
                    gnome-shell-extension-apps-menu powerline plank gnome-terminal-nautilus ",shell=True)
    if check!=0:
        sys.exit("\n\nFail Check Your Internet || Check sudo .\n\n")


    for extension in os.listdir("%s/extensions"%dirname):
        if extension not in old_extension:
            subprocess.call("cp -r %s/extensions/%s %s/.local/share/gnome-shell/extensions"%(dirname,extension,home),shell=True)



install_packs()

def check_bashrc():
	with open("%s/.bashrc"%home,"r") as myfile:
		for line in myfile.readlines():
			if "powerline-daemon" in line:
				return True
	return False

def powerline():
	if not check_bashrc():
		to_bashrc="""
if [ -f `which powerline-daemon` ]; then
	powerline-daemon -q
	POWERLINE_BASH_CONTINUATION=1
	POWERLINE_BASH_SELECT=1
	. /usr/share/powerline/bash/powerline.sh
fi
"""
		with open("%s/.bashrc"%home,"a") as myfile:
			myfile.write(to_bashrc)
		subprocess.call("source %s/.bashrc"%home,shell=True)


def fmac_themes():
	themes=["OSX-Arc-White","Gmac-Shell"]
	for theme in themes:
		subprocess.call("cp -r %s/%s  %s/.themes"%(dirname,theme,home),shell=True)

fmac_themes()



def fmac_icons():
    icons=["Gmac-icons","Gmac-Cursor","logo-top.png","Paper"]
    for i in icons:
    	subprocess.call("cp -r %s/%s   %s/.icons"%(dirname,i,home),shell=True)

fmac_icons()


def fmac_backgrounds():
    subprocess.call("cp -r %s/gnome %s/Pictures"%(dirname,home),shell=True)

fmac_backgrounds()



def fmac_plymouth():
    subprocess.call("sudo cp -r %s/mbuntu /usr/share/plymouth/themes/"%dirname,shell=True)

fmac_plymouth()




if old_extension!=None:
	for i in old_extension:
		subprocess.call("gnome-shell-extension-tool -d %s"%i,shell=True)
		time.sleep(1)



for i in extensions_to_enable:
	if os.path.isdir("%s/.local/share/gnome-shell/extensions/%s"%(home,i)) or \
    os.path.isdir("/usr/share/gnome-shell/extensions/%s"%i)or \
    os.path.isdir("/usr/local/share/gnome-shell/extensions/%s"%i):
		subprocess.call("gnome-shell-extension-tool -e  %s"%i,shell=True)
		time.sleep(1)



print ("\nPlease Wait.\n")
def fmac_plank():
	themes=["UbuntuOSXMavesemite", "Nilinca_Plank","Chrul"]
	for theme in themes:
		subprocess.call("cp -r %s/%s   %s/.local/share/plank/themes"%(dirname,theme,home),shell=True)
	
	subprocess.call("cp  -r %s/launchers  %s/.config/plank/dock1/"%(dirname,home),shell=True)
	subprocess.call("cp  %s/plank.desktop  %s/.config/autostart"%(dirname,home),shell=True)
	subprocess.call("plank &",shell=True)

fmac_plank()


for conf in gsettings:
	subprocess.call("%s"%conf,shell=True)
	time.sleep(1)
	
	
	
for conf in dconf:
    subprocess.call("%s"%conf,shell=True)
    time.sleep(1)
    
    
print ("Please do not power off or unplug your machine.\n")

subprocess.call("sudo plymouth-set-default-theme mbuntu -R",shell=True)
subprocess.call("sudo dracut -f",shell=True)



powerline()






print("\nPlease Reboot System.\n")
