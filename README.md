# Google Chrome extension and native messaging host for RIOT App Market

## Requirements
1. **sudo apt-get install git**
2. **sudo apt-get install python**
3. navigate with a terminal in to the directory where you want the extension to be stored at, then run:
   <br>**git clone https://github.com/HendrikVE/riotam-chrome-integration**

## Install Chrome extension
1. Open Chrome or Chromium
2. go to **chrome://extensions/** via the address bar
3. put a **checkmark** in **developer mode** at the top of the view
4. click on **load unpacked extension**
5. navigate in opened filebrowser to **riotam-chrome-integration/extension**
6. click on **open**

## Install Native Messaging Host
1. open a terminal
2. type **cd <to_replace>/riotam-chrome-integration/native-messaging-host**
3. run **python install_host.py --browser your_browser** (your_browser has to be replaced by **chrome** or **chromium**)

## LICENSE
* The project is licensed under the GNU Lesser General Public License
  (LGPL) version 2.1 as published by the Free Software Foundation.

All code files contain licensing information.