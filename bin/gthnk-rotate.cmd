@echo off
REM Gthnk (c) Ian Dennis Miller
REM This is a Windows batch file for launching the Gthnk rotation process.

echo "Gthnk Rotation"
set SETTINGS={{ app_data }}\Gthnk\gthnk.conf

REM The script assumes you are using a python virtualenv called 'gthnk'.
REM This script also assumes virtualenvs are in ~/Envs
cd "{{ home_directory }}\Envs\gthnk\Scripts"
.\python journal_rotate.py
