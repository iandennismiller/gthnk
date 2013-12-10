#!/bin/bash

ssl_cert=~/.gt/journal.w3n.org.pem
cookie_file=~/.gt/cookies.txt
flags="--silent --location --cookie-jar ${cookie_file} --cacert ${ssl_cert}"
journal_host="https://journal.w3n.org"

read -p "Username: " uname
stty -echo
read -p "Password: " passw; echo
stty echo

echo "Get token"
csrf=$(curl --silent --location --cookie-jar ${cookie_file} --cacert ${ssl_cert} ${journal_host}/login | grep -o "name=['\"]csrf_token['\"] .* value=['\"][^'\"]*" | sed -e "s/.*value=[\'\"]//")
data="crsf_token=${csrf}&username=${uname}&password=${passw}"
echo "success ${csrf}"

echo "logging in"
echo curl ${flags} --data $data "${journal_host}/login"
curl ${flags} --data $data "${journal_host}/login"
