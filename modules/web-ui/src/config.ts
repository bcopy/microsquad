export default {
    MQTT_HOST: process.env.MQTT_HOST || "broker.emqx.io",
    MQTT_PORT: parseInt(process.env.MQTT_PORT) || 8083,
    MQTT_CLIENT_ID: process.env.CLIENT_ID || "clientID",
}