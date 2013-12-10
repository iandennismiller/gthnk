#!/bin/bash

ssl_cert=~/.gt/journal.w3n.org.pem
cookie_file=~/.gt/cookies.txt
base_cmd="curl --silent --location --cookie-jar ${cookie_file} --cacert ${ssl_cert}"
journal_host="https://journal.w3n.org"

read -p "Username: " uname
stty -echo
read -p "Password: " passw; echo
stty echo

${base_cmd} --data "username=${uname}&password=${passw}" "${journal_host}/login"
