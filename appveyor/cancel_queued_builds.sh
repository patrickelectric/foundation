#!/usr/bin/env bash

if [ -z "$TOKEN" ]; then
    echo "Set a token with 'export TOKEN=MY_TOKEN'"
    echo "You can get your token here: https://ci.appveyor.com/api-keys"
    exit 1
fi

usage() {

cat << EOT
  usage $0 [-ahur]
        $0 -u user -r repository
  OPTIONS
    -h show this usage
    -u user
    -r repository
EOT
}

if [ "$#" -eq 0 ]; then
    usage
fi

ACCOUNT=" "
REPO=" "
while getopts "hur:" option; do
    case $option in
        h)
          usage
          exit 0
          ;;
        u)
          ACCOUNT="$OPTARG"
          ;;
        r)
          REPO="$OPTARG"
          ;;
        \?)
          echo "wrong option."
          usage
          exit 1
          ;;
    esac
done
shift $(($OPTIND - 1))


if [ "$ACCOUNT" == " " ]; then
    echo "Missing user."
    usage
fi

if [ "$REPO" == " " ]; then
    echo "Missing repository."
    usage
fi

exit 1

HEADER="Content-Type: application/json"
HEADER_DATA="Authorization: Bearer $TOKEN"

# It appears that -o will not overwrite file
curl -H $HEADER "https://ci.appveyor.com/api/projects/$ACCOUNT/$REPO/history?recordsNumber=100" > /tmp/output.json

BUILDS=$(jq --raw-output '.builds[] as $builds | $builds.status == "queued" | $builds.version' /tmp/output.json)
for build in $BUILDS; do
    echo "> Cancelling: $build"
    curl -H "$HEADER" -H "$HEADER_DATA" -X DELETE "https://ci.appveyor.com/api/builds/$ACCOUNT/$REPO/$build"
done;

# Helper to cancel a range
#for number in {4470..4869}; do
#    for name in continuous master; do
#        build=$name-$number
#        echo "> Cancelling: $build"
#        curl -H "$HEADER" -H "$HEADER_DATA" -X DELETE "https://ci.appveyor.com/api/builds/$ACCOUNT/$REPO/$build"
#    done
#done
