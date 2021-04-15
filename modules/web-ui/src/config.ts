let config = {
    MQTT_URI: process.env.MQTT_URI || "ws://broker.emqx.io:8083",
    MQTT_CLIENT_ID: process.env.CLIENT_ID || "clientID",
}

if (process.env.NODE_ENV === 'production') {
    config.MQTT_URI = "MQTT_URI_REPLACE";
    config.MQTT_CLIENT_ID = "MQTT_CLIENT_ID_REPLACE";
}

export default config;