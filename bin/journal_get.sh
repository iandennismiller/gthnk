#!/bin/bash

ssl_cert=~/.gt/journal.w3n.org.pem
cookie_file=~/.gt/cookies.txt
base_cmd="curl --silent --location --cookie ${cookie_file} --cacert ${ssl_cert}"

archive_path=~/Library/Journal/http
today=`date "+%Y-%m-%d"`
filename="${archive_path}/${today}_dump.txt"
latest="${archive_path}/latest.txt"

journal_host="https://journal.w3n.org"
${base_cmd} "${journal_host}/journal.txt" >> ${filename}
cp ${filename} ${latest}
