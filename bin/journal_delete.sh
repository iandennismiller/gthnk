#!/bin/bash

ssl_cert=~/.gt/journal.w3n.org.pem
cookie_file=~/.gt/cookies.txt
base_cmd="curl --silent --location --cookie ${cookie_file} --cacert ${ssl_cert}"

journal_host="https://journal.w3n.org"
${base_cmd} -X DELETE "${journal_host}/journal.txt"
