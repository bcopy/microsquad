#!/bin/bash
set -xe

# Ensure environment vars are set
: "${MQTT_URI?MQTT URI environment var was not set}"
: "${MQTT_TOPIC_ROOT?MQTT Topic Root was not set}"

# Replace them in bundle.js
sed -i "s/MQTT_URI_REPLACE/$MQTT_URI/g" /var/www/localhost/htdocs/js/bundle.js
sed -i "s/MQTT_TOPIC_ROOT_REPLACE/$MQTT_TOPIC_ROOT/g" /var/www/localhost/htdocs/js/bundle.js

exec "$@"