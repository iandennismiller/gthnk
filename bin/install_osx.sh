#!/bin/bash

echo "Initialize configuration"
mrbob "${VIRTUAL_ENV}/share/skels/osx" -O /tmp/gthnk_osx

echo "Installing launchd agents to $HOME/Library/LaunchAgents"
pushd /tmp/gthnk_osx
mkdir $HOME/Library/Gthnk
cp launchd/* $HOME/Library/LaunchAgents

launchctl stop com.gthnk.server

launchctl unload $HOME/Library/LaunchAgents/com.gthnk.server.plist \
    $HOME/Library/LaunchAgents/com.gthnk.librarian.plist \
    $HOME/Library/LaunchAgents/com.gthnk.dashboard.plist

launchctl load $HOME/Library/LaunchAgents/com.gthnk.server.plist \
    $HOME/Library/LaunchAgents/com.gthnk.librarian.plist \
    $HOME/Library/LaunchAgents/com.gthnk.dashboard.plist

cp gthnk.conf $HOME/Library/Gthnk/gthnk.conf
