#!/bin/bash
# gthnk (c) 2014-2016 Ian Dennis Miller

echo "Scan environment"
rm -f /tmp/gthnk_mrbob.ini
echo "[variables]" > /tmp/gthnk_mrbob.ini
echo "home_directory = ${HOME}" >> /tmp/gthnk_mrbob.ini && echo "OK"

echo "Initialize configuration"
rm -rf /tmp/gthnk_osx
mrbob "${VIRTUAL_ENV}/share/skels/osx" -c /tmp/gthnk_mrbob.ini -O /tmp/gthnk_osx && echo "OK"

echo "Create gthnk directory: $HOME/Library/Gthnk"
mkdir -v $HOME/Library/Gthnk && echo "OK"

echo "Install configuration"
cp -v /tmp/gthnk_osx/gthnk.conf $HOME/Library/Gthnk/gthnk.conf && echo "OK"

echo "Create database"
SETTINGS=$HOME/Library/Gthnk/gthnk.conf manage.py init_db && echo "OK"

echo "Create a User Account"
echo -n "username: "
read email
echo -n "password: "
read -s password
echo
echo "Creating..."
SETTINGS=$HOME/Library/Gthnk/gthnk.conf manage.py useradd -e ${email} -p ${password} && echo "OK"
unset email
unset password

echo "Installing launchd agents to $HOME/Library/LaunchAgents"
cp -v /tmp/gthnk_osx/launchd/* $HOME/Library/LaunchAgents && echo "OK"

echo "Stopping any existing gthnk server processes"
launchctl stop com.gthnk.server && echo "OK"

echo "Unloading any existing launchd configurations"
launchctl unload $HOME/Library/LaunchAgents/com.gthnk.server.plist \
    $HOME/Library/LaunchAgents/com.gthnk.librarian.plist \
    $HOME/Library/LaunchAgents/com.gthnk.dashboard.plist && echo "OK"

echo "Installing new launchd configurations"
launchctl load $HOME/Library/LaunchAgents/com.gthnk.server.plist \
    $HOME/Library/LaunchAgents/com.gthnk.librarian.plist \
    $HOME/Library/LaunchAgents/com.gthnk.dashboard.plist && echo "OK"
