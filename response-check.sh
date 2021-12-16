#!/bin/bash

count=0
started="false"

while [[ $started == "false" && $count -lt 3 ]]
do
    ((count+=1))

    echo "Starting Container [Attempt: $count]"

    response=$(curl --write-out '%{http_code}' --silent --output /dev/null http://localhost:5001/)

    if [[ $response -eq "200" ]]
    then
        started="true"
    else
        sleep 3
    fi
done

if [[ $started == "false" ]]
then
    exit 1
fi

