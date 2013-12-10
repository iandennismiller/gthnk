#!/bin/bash

GROWLNOTIFY=/usr/local/bin/growlnotify

. /usr/local/bin/virtualenvwrapper.sh
workon greenthink

$GROWLNOTIFY -n greenthink-librarian -t "web download" -m "start web download"
journal_get.sh
$GROWLNOTIFY -n greenthink-librarian -t "web download" -m "finish web download"
journal_delete.sh

# journal_merge.py

$GROWLNOTIFY -n greenthink-librarian -t "rotation" -m "start rotation"
journal_rotate.py
$GROWLNOTIFY -n greenthink-librarian -t "rotation" -m "finish rotation"

# journal_actions.py
