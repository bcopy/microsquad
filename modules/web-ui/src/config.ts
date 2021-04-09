let config = {
    MQTT_HOST: process.env.MQTT_HOST || "broker.emqx.io",
    MQTT_PORT: process.env.MQTT_PORT || "8083",
    MQTT_CLIENT_ID: process.env.CLIENT_ID || "clientID",
}

if (process.env.NODE_ENV === 'production') {
    config.MQTT_HOST = "MQTT_HOST_REPLACE";
    config.MQTT_PORT = "MQTT_PORT_REPLACE";
    config.MQTT_CLIENT_ID = "MQTT_CLIENT_ID_REPLACE";
}

export default config;