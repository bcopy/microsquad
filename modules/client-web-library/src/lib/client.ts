import { MQTTSubject } from 'musquette'
import { Subject } from 'rxjs'
import { filter } from 'rxjs/operators'


export enum MqttMicrosquadEventType {
    PLAYER_UPDATE,
    TEAM_UPDATE,
    SCOREBOARD_UPDATE,
    GAME_UPDATE,
    OTHER
 }
 
 export class MqttUpdateEvent {
     type: MqttMicrosquadEventType;
     id: string;
     property: string;
     newValue: any;
     oldValue: any;
 
     constructor(type : MqttMicrosquadEventType = MqttMicrosquadEventType.OTHER,id?:string, property?:string, newValue : any = null, oldValue : any = null ){
         this.type = type;
         this.id = id!;
         this.property = property!;
         this.newValue = newValue;
         this.oldValue = oldValue;
     }

 }
 const PLAYER_NODE_PREFIX = "player-";
 const TEAM_NODE_PREFIX = "team-";
 const SCOREBOARD_NODE_PREFIX = "scoreboard";
//  const GAME_NODE_PREFIX = "game";

// export function deserialize(message : any) : MqttUpdateEvent {
//     var result = new MqttUpdateEvent();
//     let topic = message.topic.substring(mqttSubscriptionRoot.length-1);
//     let topicParts = topic.split("/");

//     // Only interpret gateway-related messages that are not meta-topics
//     if (topicParts[0] == "gateway" && (!topicParts.slice(-1)[0].startsWith("$"))) {
//         const nodeName = topicParts[1];

//         if (nodeName.startsWith(PLAYER_NODE_PREFIX)){
//             result.type = MqttMicrosquadEventType.PLAYER_UPDATE;
//             result.id = nodeName.substring(PLAYER_NODE_PREFIX.length);
//             result.property = topicParts[2];
//             result.newValue = message.message;
//         }
//         else if(nodeName.startsWith(TEAM_NODE_PREFIX)){
//             result.type = MqttMicrosquadEventType.TEAM_UPDATE;
//             result.id = nodeName.substring(TEAM_NODE_PREFIX.length);
//             result.property = topicParts[2];
//             result.newValue = message.message;
//         }
//         else if (topicParts[1].startsWith(SCOREBOARD_NODE_PREFIX)){
//             result.type = MqttMicrosquadEventType.SCOREBOARD_UPDATE;
//             result.property = topicParts[2];
//             result.newValue = message.message;
//         }
//     }
//     return result;
// }

export class MicrosquadClient {
    uri : string
    mqtt : MQTTSubject<MqttUpdateEvent>
    playerSubject$ : Subject<any>
    mqttSubscriptionRoot : string
    // teamSubject$ : Subject<MqttUpdateEvent>
    // scoreboardSubject$ : Subject<MqttUpdateEvent>

    

    constructor (uri: string, clientID : string, mqttSubscriptionRoot: string) {
        this.uri = uri;
        this.mqttSubscriptionRoot = mqttSubscriptionRoot;
        var clientDeserializer = this.deserialize
        this.mqtt = new MQTTSubject({
            url: uri,
            // mqtt.js options
            options: {
                keepalive: 3000,
                clientId: clientID
            }
            ,deserializer: clientDeserializer
        })

        this.playerSubject$ = new Subject();

        this.mqtt.pipe(filter(event => event.message.type == MqttMicrosquadEventType.PLAYER_UPDATE))
                 .subscribe(this.playerSubject$)

        // // Callback handlers
        // this.client.onConnectionLost = connectionLostCallback || this._onConnectionLost;
        // this.client.onMessageArrived = messageArrivedCallback;

        // this.client.connect({
        //     timeout: 10,
        //     onSuccess: onConnectCallback || this._onConnect,
        //     onFailure: this._onFailure,
        //     reconnect: true,
        // });
    }

    
    _onConnect() {
        // console.log("Successfully Connected");
    }
      
    _onConnectionLost(_responseObject : any) {
        // if (responseObject.errorCode !== 0) {
        //     console.error("Connection lost: " + responseObject.errorMessage);
        // }
    }

    _onFailure(_message : any) {
        // console.error("Connection failed: " + message);
    }

    deserialize(message : any) : MqttUpdateEvent {
        var result = new MqttUpdateEvent();
        let topic = message.topic.substring(this.mqttSubscriptionRoot.length-1);
        let topicParts = topic.split("/");
    
        // Only interpret gateway-related messages that are not meta-topics
        if (topicParts[0] == "gateway" && (!topicParts.slice(-1)[0].startsWith("$"))) {
            const nodeName = topicParts[1];
    
            if (nodeName.startsWith(PLAYER_NODE_PREFIX)){
                result.type = MqttMicrosquadEventType.PLAYER_UPDATE;
                result.id = nodeName.substring(PLAYER_NODE_PREFIX.length);
                result.property = topicParts[2];
                result.newValue = message.message;
            }
            else if(nodeName.startsWith(TEAM_NODE_PREFIX)){
                result.type = MqttMicrosquadEventType.TEAM_UPDATE;
                result.id = nodeName.substring(TEAM_NODE_PREFIX.length);
                result.property = topicParts[2];
                result.newValue = message.message;
            }
            else if (topicParts[1].startsWith(SCOREBOARD_NODE_PREFIX)){
                result.type = MqttMicrosquadEventType.SCOREBOARD_UPDATE;
                result.property = topicParts[2];
                result.newValue = message.message;
            }
        }
        return result;
    }

    // publish(topic : string, payload : string) {
    //     console.log("Sending message:\nTopic: " + topic +"\nPayload: " + payload);
      
    //     let message = new MQTT.Message(payload);
    //     message.destinationName = topic;
      
    //     this.client.send(message);
    // }

    // subscribe(topic : string) {
    //     // let subs = document.getElementById('subscriptions');
    //     // subs.innerHTML += "Subscribed to " + topic + "<br />";
      
    //     console.log("MQTT : Subscribed to " + topic);
    //     this.client.subscribe(topic);
    // }
}
