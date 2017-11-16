#!/bin/bash
# gthnk (c) 2014-2016 Ian Dennis Miller

echo "Stopping any existing gthnk server processes"
launchctl stop com.gthnk.server && echo "OK"

echo "Unloading any existing launchd configurations"
launchctl unload $HOME/Library/LaunchAgents/com.gthnk.server.plist \
    $HOME/Library/LaunchAgents/com.gthnk.librarian.plist \
    $HOME/Library/LaunchAgents/com.gthnk.dashboard.plist && echo "OK"
