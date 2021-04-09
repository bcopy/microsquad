#!/bin/bash
set -xe

# Ensure environment vars are set
: "${MQTT_HOST?environment var was not set}"
: "${MQTT_PORT?environment var was not set}"
: "${MQTT_CLIENT_ID?environment var was not set}"

# Replace them in bundle.js
sed -i "s/MQTT_HOST_REPLACE/$MQTT_HOST/g" /var/www/localhost/htdocs/js/bundle.js
sed -i "s/MQTT_PORT_REPLACE/$MQTT_PORT/g" /var/www/localhost/htdocs/js/bundle.js
sed -i "s/MQTT_CLIENT_ID_REPLACE/$MQTT_CLIENT_ID/g" /var/www/localhost/htdocs/js/bundle.js

exec "$@"