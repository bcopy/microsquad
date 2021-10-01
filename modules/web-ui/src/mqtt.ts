import * as MQTT from 'paho-mqtt';

export class MQTTClient {
    client : MQTT.Client;
    uri : string;

    constructor (uri: string, clientID : string, messageArrivedCallback : (message : MQTT.Message) => void, onConnectCallback? : () => void, connectionLostCallback? : (response: any) => void) {
        this.uri = uri;
        this.client = new MQTT.Client(uri, clientID);
        

        // Callback handlers
        this.client.onConnectionLost = connectionLostCallback || this._onConnectionLost;
        this.client.onMessageArrived = messageArrivedCallback;

        this.client.connect({
            timeout: 10,
            onSuccess: onConnectCallback || this._onConnect,
            onFailure: this._onFailure,
            reconnect: true,
        });
    }

    _onConnect() {
        console.log("Succesfully Connected");
    }
      
    _onConnectionLost(responseObject : any) {
        if (responseObject.errorCode !== 0) {
            console.error("Connection lost: " + responseObject.errorMessage);
        }
    }

    _onFailure(message : any) {
        console.error("Connection failed: " + message);
    }

    publish(topic : string, payload : string) {
        console.log("Sending message:\nTopic: " + topic +"\nPayload: " + payload);
      
        let message = new MQTT.Message(payload);
        message.destinationName = topic;
      
        this.client.send(message);
    }

    subscribe(topic : string) {
        let subs = document.getElementById('subscriptions');
        subs.innerHTML += "Subscribed to " + topic + "<br />";
      
        this.client.subscribe(topic);
    }
}

export enum MqttMicrosquadEventType {
   PLAYER_UPDATE,
   TEAM_UPDATE,
   SCOREBOARD_UPDATE,
   GAME_UPDATE
}

export class MqttUpdateEvent {
    type: MqttMicrosquadEventType;
    id: string;
    property: string;
    newValue: any;
    oldValue: any;

    constructor(type : MqttMicrosquadEventType,id:string, property:string, newValue, oldValue = null ){
        this.type = type;
        this.id = id;
        this.property = property;
        this.newValue = newValue;
        this.oldValue = oldValue;
    }
}