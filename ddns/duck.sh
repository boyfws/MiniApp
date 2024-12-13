#!/bin/sh

DOMAINS="mini-app-test-prikol"
TOKEN="$DUCK_TOKEN"

if [ -z "$TOKEN" ]; then
    echo "Error: DUCK_TOKEN environment variable is not set."
    exit 1
fi

update_duckdns() {
    url="https://www.duckdns.org/update?domains=${DOMAINS}&token=${TOKEN}"

    curl_out=$(/usr/bin/curl --insecure --silent "$url")

    if [ "$curl_out" = "OK" ]; then
        echo "$(date): duckdns update ok"
    else
        echo "$(date): duckdns update failed"
    fi
}

while true; do
    update_duckdns
    sleep 300
done