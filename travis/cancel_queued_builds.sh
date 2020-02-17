#!/usr/bin/env bash

if [ -z "$TOKEN" ]; then
    echo "Set a token with 'export TOKEN=MY_TOKEN'"
    echo "You can get your token here: https://travis-ci.org/account/preferences?utm_medium=notification&utm_source=github_status"
    exit 1
fi

usage() {

cat << EOT
  usage $0 [-hi]
        $0 -i repository_id
  OPTIONS
    -h show this usage
    -i repository_id
EOT
}

if [ "$#" -eq 0 ]; then
    usage
fi

REPOSITORY_ID=" "
while getopts "hi:" option; do
    case $option in
        i)
          REPOSITORY_ID="$OPTARG"
          ;;
        h)
          usage
          exit 0
          ;;
        \?)
          echo "wrong option."
          usage
          exit 1
          ;;
    esac
done
shift $(($OPTIND - 1))


if [ "$REPOSITORY_ID" == " " ]; then
    echo "Missing repository ID."
    usage
fi

HEADER="Content-Type: application/json"
HEADER_DATA="Authorization: Bearer $TOKEN"

while true; do
    # It appears that -o will not overwrite file
    curl -H "Travis-API-Version: 3" \
        -H "Content-Type: application/json" \
        -H "Authorization: token $TOKEN" \
        "https://api.travis-ci.org/repo/$REPOSITORY_ID/builds?limit=1000&state=started&event_type=push" > /tmp/output.json

    if [ $(jq --raw-output '.builds | length' /tmp/output.json ) -eq 0 ]; then
        break
    fi

    BUILDS=$(jq --raw-output '.builds[] as $builds | $builds.id' /tmp/output.json)
    for build in $BUILDS; do
        echo "> Cancelling: $build"
        curl -H "Travis-API-Version: 3" \
            -H "Content-Type: application/json" \
            -H "Authorization: token $TOKEN" \
            -X POST "https://api.travis-ci.org/build/${build}/cancel"
    done;
done;

echo 'All Done!'
