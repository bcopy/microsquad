import * as MQTT from 'paho-mqtt';
import { Subject } from 'rxjs';

export class MQTTClient {
    client : MQTT.Client
    uri : string
    playerSubject : Subject<MqttUpdateEvent>
    teamSubject : Subject<MqttUpdateEvent>
    scoreboardSubject : Subject<MqttUpdateEvent>

    mqttTopicRoot : string
    mqttSubscriptionRoot : string

    gameName : string = ""

    constructor (uri: string
            , clientID : string
            , mqttTopicRoot : string 
            , gameName : string
            , playerSubject?: Subject<MqttUpdateEvent>
            , teamSubject?: Subject<MqttUpdateEvent>
            , scoreboardSubject?: Subject<MqttUpdateEvent>) {
        this.uri = uri;
        this.client = new MQTT.Client(uri, clientID);

        this.playerSubject = playerSubject
        this.teamSubject = teamSubject
        this.scoreboardSubject = scoreboardSubject
        this.gameName = gameName
        this.mqttTopicRoot = mqttTopicRoot
        this.mqttSubscriptionRoot = mqttTopicRoot+"/#"
        

        // Callback handlers
        this.client.onConnectionLost = this._onConnectionLost.bind(this);
        this.client.onMessageArrived = this._onMessageArrived.bind(this);

        var mqttClient = this;
        this.client.connect({
            timeout: 10,
            onSuccess: this._onConnect.bind(this),
            onFailure: this._onFailure.bind(this),
            reconnect: true,
        });
    }

    _onMessageArrived(message : any) {
        this._mqttCommandHandler(message.destinationName, message.payloadString);
    }

    _onConnect() {
        console.log("Successfully connected");
        setTimeout(function(mqttClient){
            mqttClient.client.subscribe(mqttClient.mqttSubscriptionRoot);
            // Update the game name
            mqttClient._updateGameNameViaMQTT();
        },500, this);
        
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
        // let subs = document.getElementById('subscriptions');
        // subs.innerHTML += "Subscribed to " + topic + "<br />";
      
        console.log("MQTT : Subscribed to " + topic);
        this.client.subscribe(topic);
    }

    _mqttCommandHandler(incomingTopic, value:string) {
        let topic = incomingTopic.substring(this.mqttSubscriptionRoot.length-1);
        let topicParts = topic.split("/");
    
        if(topicParts.slice(-1)[0].startsWith("$")){
            // This incoming message is a homie metadata topic, we can ignore it
            return;
        }
    
        if (topicParts[0] == "gateway") {
            const PLAYER_NODE_PREFIX = "player-";
            const TEAM_NODE_PREFIX = "team-";
            const SCOREBOARD_NODE_PREFIX = "scoreboard";
            const GAME_NODE_PREFIX = "game";
    
            const nodeName = topicParts[1];
            /////////////
            // If the message concerns a player or a team, we store its state for later reference
            // Eventually, we could keep it in a store implementation - for the time being, maps of maps
            if (nodeName.startsWith(PLAYER_NODE_PREFIX) ||
            nodeName.startsWith(TEAM_NODE_PREFIX) ) {
                let devicePrefix : string;
                let stateMap : Map<string,any>;
                let propertyName : string;
                let eventType : MqttMicrosquadEventType;
                let subject: Subject<MqttUpdateEvent>;
                if (nodeName.startsWith(PLAYER_NODE_PREFIX)) {
                    devicePrefix = PLAYER_NODE_PREFIX;
                    // stateMap = playerStates;
                    eventType = MqttMicrosquadEventType.PLAYER_UPDATE;
                    subject = this.playerSubject;
                } else if (nodeName.startsWith(TEAM_NODE_PREFIX)) {
                    devicePrefix = TEAM_NODE_PREFIX;
                    // stateMap = teamStates;
                    eventType = MqttMicrosquadEventType.TEAM_UPDATE;
                    subject = this.teamSubject;
                }
                if (devicePrefix != null) {
                    let deviceId = nodeName.substring(devicePrefix.length);
                    let propertyName = topicParts[2];
                    // let state = stateMap.get(deviceId) ?? new Map();
                    // state.set(propertyName, value);
                    // stateMap.set(deviceId, state);
    
                    subject.next(new MqttUpdateEvent(eventType, deviceId, propertyName, value));
                }
            } else if (topicParts[1].startsWith(SCOREBOARD_NODE_PREFIX)){
                this.scoreboardSubject.next(new MqttUpdateEvent(MqttMicrosquadEventType.SCOREBOARD_UPDATE, null, topicParts[2], value));
            } else if (topicParts[1].startsWith(GAME_NODE_PREFIX)){
                // If the list of transitions available has changed, add buttons allowing to trigger them by modifying "fire-transition"
                if(topicParts[2] == "transitions"){
                    var controlsDiv = <HTMLDivElement>document.getElementById("transition-controls");
                    controlsDiv.innerHTML="";
                    if(value.trim() != ""){
                        value.split(",").forEach(transition => {
                            var transitionButton : HTMLAnchorElement = <HTMLAnchorElement>document.createElement("a");
                            transitionButton.classList.add("btn", "btn-primary", "btn-sm");
                            transitionButton.setAttribute("role", "button");
                            transitionButton.innerHTML = transition;
                            transitionButton.setAttribute("data-transition-name", transition);
                            transitionButton.addEventListener('click', event => { 
                                    var trns = (event.target as Element).getAttribute("data-transition-name");
                                    console.log("firing transition "+trns);
                                    this.fireTransitionViaMQTT(trns)
                            });
                            controlsDiv.appendChild(transitionButton);
                        });
                    }
                }
    
            }
    
            //
            ////////////////
        }
    
    }

    _updateGameNameViaMQTT(){
        this.publish(this.mqttTopicRoot + "/gateway/game/name/set", this.gameName);
    }

    fireTransitionViaMQTT(transition){
        this.publish(this.mqttTopicRoot + "/gateway/game/fire-transition/set", transition);
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