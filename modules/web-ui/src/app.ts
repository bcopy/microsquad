import * as THREE from "three";
import { Subject } from 'rxjs';
import { MQTTClient, MqttMicrosquadEventType,MqttUpdateEvent } from "./mqtt";
import { PlayerManager } from './playerManager';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
import { Context, UpdateObject } from "./updateObject";
import envConfig from './config';
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader";
import { Player } from "./player";
import { Scoreboard } from "./scoreboard";

var config = envConfig;

var assetsConfig : any;

var mqttTopicRoot : string;

var mqttClient :MQTTClient;

var mqttClientId : string;

const playerSubject : Subject<MqttUpdateEvent> = new Subject();
const teamSubject : Subject<MqttUpdateEvent> = new Subject();
const scoreboardSubject : Subject<MqttUpdateEvent> = new Subject();

var sessionCode = "session-default";

var mqttSubscriptionRoot:string;

var playerStates = new Map();
var teamStates = new Map();

const loader = new THREE.FileLoader();


function startMqttSubscriptions(){
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(window.location.search);
    sessionCode = urlParams.get('sc') ?? "session-default";
    const urlClientId = urlParams.get('ci');
    if (urlClientId != null) {
        mqttClientId = "microsquad-web:" + urlClientId; // if specified in the URL, retain the same client ID
    }
    else {
        mqttClientId = "microsquad-web:" + Math.random().toString(36).substr(2, 5); // unique client ID to prevent reconnect loop
    }

    mqttClient = new MQTTClient(
        config.MQTT_URI,
        mqttClientId,
        onMessageArrived,
        onMqttConnect,
        onMqttConnectionLost,
    );
}

var assetsInitialized:boolean = false;

loader.load('assets/assets.json',
    function ( data ) {
        assetsConfig = JSON.parse(<string>data);

        //load a text file and output the result to the console
        loader.load(
            // resource URL
            'conf/config.json',

            // onLoad callback
            function ( data ) {
                config = JSON.parse(<string>data);
                initializeAssetsSettings();
                startMqttSubscriptions();

            },
            undefined,
            // onError callback
            function ( err ) {
                console.error( 'Could not load JSON configuration at conf/config.json - using Node env configuration' );
                initializeAssetsSettings();
                startMqttSubscriptions();
            }
        );
        
    },
    undefined,
    // onError callback
    function ( err ) {
        console.error( 'Could not load assets JSON configuration at assets/assets.json' );
    }
)




/////////////////////////////////////////// SCENE SETUP ////////////////////////////////////////////

function fitCameraToObject( cam : THREE.PerspectiveCamera, object : THREE.Object3D, offset?: number, cntrls? : OrbitControls ) {

    offset = offset || 1.1;
    const boundingBox = new THREE.Box3();

    // get bounding box of object - this will be used to setup controls and camera
    boundingBox.setFromObject( object );
    const center = new THREE.Vector3()
    boundingBox.getCenter(center);
    const size = boundingBox.getSize(center);

    // get the max side of the bounding box (fits to width OR height as needed )
    const maxDim = Math.max( size.x, size.y, size.z );
    const fov = cam.fov * ( Math.PI / 180 );
    let camZ = Math.abs( maxDim / 4 * Math.tan( fov * 2 ) );

    camZ *= offset; // zoom out a little so that objects don't fill the screen
    cam.position.z = camZ;

    const minZ = boundingBox.min.z;
    const cameraToFarEdge = ( minZ < 0 ) ? -minZ + camZ : camZ - minZ;

    cam.far = cameraToFarEdge * 3;
    cam.updateProjectionMatrix();

    if ( cntrls ) {
      // set camera to rotate around center of loaded object
      cntrls.target = center;
      // prevent camera from zooming out far enough to create far plane cutoff
      cntrls.maxDistance = cameraToFarEdge * 2;
      cntrls.saveState();
    } else {
        cam.lookAt( center )
   }
}

const renderer = new THREE.WebGLRenderer(  {antialias: true } );
renderer.setPixelRatio( window.devicePixelRatio );
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap; 
renderer.outputEncoding = THREE.sRGBEncoding;
document.body.appendChild(renderer.domElement);

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x418afb); 
const ambientColor = 0xFFFFC5;
const ambiIntensity = 0.7;
const ambilight = new THREE.AmbientLight(ambientColor, ambiIntensity);

const geo = new THREE.CircleGeometry(20, 20, 32);
const mat = new THREE.MeshStandardMaterial({ color: 0xe4ca4c, side: THREE.DoubleSide });
var plane = new THREE.Mesh(geo, mat);
plane.receiveShadow = true;
plane.rotateX( - Math.PI / 2);
scene.add(plane);

const dirColor = 0xffffaa;
const dirIntensity = 0.7;
const dirlight = new THREE.DirectionalLight(dirColor, dirIntensity);
dirlight.position.set(0,2,0);
dirlight.castShadow = true;
const helper = new THREE.DirectionalLightHelper(dirlight);

const clock = new THREE.Clock();
var objects: UpdateObject[] = [];


const camera = new THREE.PerspectiveCamera(
    45,                                         // FOV
    window.innerWidth / window.innerHeight,     // Ratio
    0.1, 1000                                   // Near / Far Clip
);
camera.position.set(0, 0, -6);
// camera.zoom = 20;

const controls = new OrbitControls( camera, renderer.domElement );
controls.enableDamping = false;
// controls.dampingFactor = 0.1;
controls.enablePan = false;
controls.target.set(0, 4, 1);
controls.minPolarAngle = controls.getPolarAngle();
controls.maxPolarAngle = controls.getPolarAngle();
controls.maxAzimuthAngle = controls.getAzimuthalAngle();
controls.minAzimuthAngle = controls.getAzimuthalAngle();
// let dist = camera.position.distanceTo(controls.target);
controls.maxDistance = 10;
camera.updateMatrixWorld();

var context : Context = {
    scene: scene,
    camera: camera,
    renderer: renderer,
    objList: objects,
};
UpdateObject.context = context;

var playerManager = new PlayerManager(playerSubject);

window['playerManager'] = playerManager;

var addPlayerButton : HTMLButtonElement = <HTMLButtonElement>document.getElementById("add-player");
addPlayerButton.addEventListener('click', () => { playerManager.addPlayer("Player:"+ Math.random().toString(36).substr(2, 5), true) });


var zoomScreenButton : HTMLButtonElement = <HTMLButtonElement>document.getElementById("zoom-screen");
zoomScreenButton.addEventListener('click', () => { fitCameraToObject(camera,scoreboard.mesh) });

var scoreboard = new Scoreboard(UpdateObject.context, scoreboardSubject);

window['scoreboard'] = scoreboard;
////////////////////////////////////////// ASSET LOADING ///////////////////////////////////////////

const manager = new THREE.LoadingManager();

manager.onStart = () => {
    console.log("Load start...");
}

manager.onProgress = ( url, itemsLoaded, itemsTotal ) => {
    console.log(`Loading (${itemsLoaded}/${itemsTotal}): ${url}`);
}

manager.onError = (url) => {
    console.log(`Error loading: ${url}`);
};

// Animations in gltf.animations that need to be looped
interface AnimationInfo {
    animation : THREE.AnimationClip,
    loop : boolean,
}

const gltfLoader = new GLTFLoader(manager);

const asset_url = "assets/characterMediumAllAnimations.glb"; 
var playerSkins = {};
var loopedAnimations = [];
var accessories = {};

///////////// CHARACTER & ANIMATIONS /////////////
function initializeAssetsSettings(){
    ///////////////// SKIN TEXTURES //////////////////

    var texLoader = new THREE.TextureLoader(manager);

    let skin_names = assetsConfig.skins;

    let playerSkins = {};
    skin_names.forEach(skin => {
        let map = texLoader.load("assets/skins/" + skin +".png");
        map.encoding = THREE.sRGBEncoding;
        map.flipY = false;
        playerSkins[skin] = map;
    });

    loopedAnimations = assetsConfig.animations.attitudes;

    gltfLoader.load(asset_url, ( gltf ) => {

        Player.gltf = gltf;

        gltf.scene.traverse( function( node ) {
            if ( node.isObject3D ) { node.castShadow = true; }
        } );
    
        gltf.animations.forEach(anim => {
    
            let animInfo : AnimationInfo = {
                animation : anim,
                loop : loopedAnimations.includes(anim.name),
            };
    
            Player.animations[anim.name] = animInfo;
    
        });
    
    });

    for (var accessory in assetsConfig.accessories) {
        let url = `assets/accessories/${accessory}.glb`
        gltfLoader.load(url, (gltf) => {
            let filename = url.split("/").pop();
            let accessoryName = filename.split(".")[0];
            accessories[accessoryName] = assetsConfig.accessories[accessoryName]
            accessories[accessoryName].scene = gltf.scene;
        });
    }
    manager.onLoad = () => {
        Player.accessories = assetsConfig.accessories;
        Player.skins = playerSkins;
    }

    setupThreeJsScene();
}



function setupThreeJsScene(){

    ///////////////////////////////////////////// LIGHTING /////////////////////////////////////////////

    // Ambient Light
    ambilight.visible = true;
    scene.add(ambilight);

    // Directional light
    dirlight.position.set(0, 10, 0);
    dirlight.target.position.set(2, 4, 6);
    scene.add(dirlight);
    scene.add(dirlight.target);
    dirlight.visible = true;
    helper.visible = false;
    scene.add(helper);

    ////////////////////////////////////// RENDERING & ANIMATION ///////////////////////////////////////

    window.addEventListener('resize', onWindowResize, false);
    function onWindowResize() {
        // recalculate camera zoom
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
        render();
    }

    var animate = function () {
        requestAnimationFrame(animate);

        var delta = clock.getDelta();
        controls.update();

        objects.forEach(obj => {
            obj.update(delta);
        });

        render();
    };

    function render() {
        renderer.render(scene, camera);
    }
    animate();
}

///////////////////////////////////////// COMMAND HANDLING /////////////////////////////////////////

function onMessageArrived(message : any) {
    commandHandler(message.destinationName, message.payloadString);
}

// function teamCommandHandler(command: string[], teamID: string) {

//     switch (command[0]) {

//         case _cmdStringChangeSkin:
//         case _cmdStringChangeAnimation:
//         case _cmdStringSay:
//         case _cmdStringChangeAccessory:
//         case _cmdStringAssignTeam:
//             // Run command for every player in team
//             if (!(teamID in playerManager.teams)) {
//                 console.warn(`Team "${teamID}" does not exist`);
//             } else {
//                 playerManager.teams[teamID].players.forEach( (player) => {
//                     playerCommandHandler(command, player.id);
//                 });
//             }         
//             break;
    
//         case _cmdStringSplitTeams:
//             let teamNames = command.splice(1);   
//             let i = 0;
//             let tot = Object.keys(playerManager.players).length;
//             for (let playerName in playerManager.players) {
//                 playerManager.assignTeam(playerName, teamNames[Math.floor(i/tot * teamNames.length)]);
//                 i++;
//             }
//             break;

//         case "reset":
//             // If teamID is not specified, reset all teams
//             if (teamID) {

//                 if (!(teamID in playerManager.teams)) {
//                     console.warn(`Team "${teamID}" does not exist`);
//                 } else {
//                     playerManager.teams[teamID].players.forEach(player => {
//                         playerManager.assignTeam(player.id, playerManager.defaultTeam.name);
//                     });
//                 }

//             } else {
//                 for (let playerName in playerManager.players) {
//                     playerManager.assignTeam(playerName, playerManager.defaultTeam.name);
//                 }
//             }
//             break;

//         default:
//             break;
//     }
// }


function commandHandler(incomingTopic, value) {
    let topic = incomingTopic.substring(mqttSubscriptionRoot.length-1);
    let topicParts = topic.split("/");

    if(topicParts.slice(-1)[0].startsWith("$")){
        // This incoming message is a homie metadata topic, we can ignore it
        return;
    }

    if (topicParts[0] == "gateway") {
        const PLAYER_NODE_PREFIX = "player-";
        const TEAM_NODE_PREFIX = "team-";
        const SCOREBOARD_NODE_PREFIX = "scoreboard";

        /////////////
        // If the message concerns a player or a team, we store its state for later reference
        // Eventually, we could keep it in a store implementation - for the time being, maps of maps
        if (topicParts[1].startsWith(PLAYER_NODE_PREFIX) ||
            topicParts[1].startsWith(TEAM_NODE_PREFIX) ) {
            let devicePrefix : string;
            let stateMap : Map<string,any>;
            let propertyName : string;
            let eventType : MqttMicrosquadEventType;
            let subject: Subject<MqttUpdateEvent>;
            if (topicParts[1].startsWith(PLAYER_NODE_PREFIX)) {
                devicePrefix = PLAYER_NODE_PREFIX;
                stateMap = playerStates;
                eventType = MqttMicrosquadEventType.PLAYER_UPDATE;
                subject = playerSubject;
            } else if (topicParts[1].startsWith(TEAM_NODE_PREFIX)) {
                devicePrefix = TEAM_NODE_PREFIX;
                stateMap = teamStates;
                eventType = MqttMicrosquadEventType.TEAM_UPDATE;
                subject = teamSubject;
            }
            if (devicePrefix != null) {
                let deviceId = topicParts[1].substring(devicePrefix.length);
                let propertyName = topicParts[2];
                let state = stateMap.get(deviceId) ?? new Map();
                state.set(propertyName, value);
                stateMap.set(deviceId, state);

                subject.next(new MqttUpdateEvent(eventType, deviceId, propertyName, value));
            }
        } else if (topicParts[1].startsWith(SCOREBOARD_NODE_PREFIX)){
            scoreboardSubject.next(new MqttUpdateEvent(MqttMicrosquadEventType.SCOREBOARD_UPDATE, null, topicParts[2], value));
        }

        //
        ////////////////
    }

}

function onMqttConnect() {
    console.log("Connected to " + mqttClient.uri);
    if(config.MQTT_TOPIC_ROOT != null){
        mqttTopicRoot = config.MQTT_TOPIC_ROOT
    }
    mqttSubscriptionRoot = mqttTopicRoot +"/"+sessionCode+"/#";
    setTimeout(function(){mqttClient.subscribe(mqttSubscriptionRoot)},500);
    // subButton.disabled = false;
    // pubButton.disabled = false;
}

function onMqttConnectionLost(response) {
    if (response.errorCode !== 0) {
        console.error("Connection lost: " + response.errorMessage);
        // subButton.disabled = true;
        // pubButton.disabled = true;
    }
}

// function _btnPublish() {
//     let topic = (<HTMLInputElement>document.getElementById("pub-topic")).value;
//     let payload = (<HTMLInputElement>document.getElementById("pub-payload")).value;
//     mqttClient.publish(topic, payload);
// }

// function _btnSubscribe() {
//     let topic = (<HTMLInputElement>document.getElementById("sub-topic")).value;
//     mqttClient.subscribe(topic);
// }