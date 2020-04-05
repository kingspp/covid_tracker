#!/bin/bash

# Check if curl exists
if ! [ -x "$(command -v curl)" ]; then
  echo "{\"error\":\"date binary not found\"}"
  exit 1
fi


GLOBAL_STATS=$(curl -sS "https://corona.lmao.ninja/all")

INDIA_STATS=$(curl -sS --request GET --url 'https://api.covid19india.org/data.json')

MYS_STATS=$(curl -sS --request GET --url 'https://api.covid19india.org/state_district_wise.json')

ALL_STATS=$(curl -sS "https://www.bing.com/covid/data")

echo $(cat <<-EOF
{
  "global":$GLOBAL_STATS,
  "ind":$INDIA_STATS,
  "mys":$MYS_STATS,
  "all":$ALL_STATS
}
EOF
)