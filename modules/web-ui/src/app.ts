import * as THREE from "three";
import { MQTTClient } from "./mqtt";
import { PlayerManager } from './playerManager';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
import { Context, UpdateObject } from "./updateObject";
import envConfig from './config';
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader";
import { Player } from "./player";
import Accessories from './accessories.json';
import { Billboard } from "./billboard";

var config = envConfig;

var mqttclient;

const loader = new THREE.FileLoader();

function startMqttSubscriptions(){

    mqttclient = new MQTTClient(
        config.MQTT_URI,
        config.MQTT_CLIENT_ID + ":" + Math.random().toString(36).substr(2, 5), // unique clientID to prevent reconnect loop
        onMessageArrived,
        onMQTTConnect,
        onMQTTConnectionLost,
    );
}


//load a text file and output the result to the console
loader.load(
	// resource URL
	'conf/config.json',

	// onLoad callback
	function ( data ) {
		config = JSON.parse(<string>data);
        startMqttSubscriptions();
	},
    undefined,
    // onError callback
	function ( err ) {
		console.error( 'Could not load JSON configuration at conf/config.json - using Node env configuration' );
        startMqttSubscriptions();
	}
);


//////////////////////////////////////////// MQTT SETUP ////////////////////////////////////////////


// Connect subscribe & publish buttons
var subButton : HTMLButtonElement = <HTMLButtonElement>document.getElementById("subscribe-button");
subButton.addEventListener('click', () => { _btnSubscribe() } );

var pubButton : HTMLButtonElement = <HTMLButtonElement>document.getElementById("publish-button");
pubButton.addEventListener('click', () => { _btnPublish() } );



/////////////////////////////////////////// SCENE SETUP ////////////////////////////////////////////

const renderer = new THREE.WebGLRenderer( {antialias: true} );
renderer.setPixelRatio( window.devicePixelRatio );
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.outputEncoding = THREE.sRGBEncoding;
document.body.appendChild(renderer.domElement);

const scene = new THREE.Scene();
scene.background = new THREE.Color(0xf5ca6e);

const clock = new THREE.Clock();
var objects: UpdateObject[] = [];


const camera = new THREE.PerspectiveCamera(
    45,                                         // FOV
    window.innerWidth / window.innerHeight,     // Ratio
    0.1, 1000                                   // Near / Far Clip
);
camera.position.set(0, 2, -10);

const controls = new OrbitControls( camera, renderer.domElement );
controls.enableDamping = true;
controls.dampingFactor = 0.1;
controls.enablePan = false;
controls.target.set(0, 2, 1);
controls.minPolarAngle = controls.getPolarAngle();
controls.maxPolarAngle = controls.getPolarAngle();
controls.maxAzimuthAngle = controls.getAzimuthalAngle();
controls.minAzimuthAngle = controls.getAzimuthalAngle();
let dist = camera.position.distanceTo(controls.target);
controls.maxDistance = 100;
camera.updateMatrixWorld();

var context : Context = {
    scene: scene,
    camera: camera,
    renderer: renderer,
    objList: objects,
};
UpdateObject.context = context;

var playerManager = new PlayerManager();
var addPlayerButton : HTMLButtonElement = <HTMLButtonElement>document.getElementById("add-player");
addPlayerButton.addEventListener('click', () => { playerManager.addPlayer("Player:"+ Math.random().toString(36).substr(2, 5)) });

var billboard = new Billboard(UpdateObject.context);


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

///////////////// SKIN TEXTURES //////////////////

var texLoader = new THREE.TextureLoader(manager);

let skin_files = ['alienA.png', 'alienB.png', 'animalA.png', 'animalB.png', 'animalBaseA.png', 'animalBaseB.png', 'animalBaseC.png', 'animalBaseD.png', 'animalBaseE.png', 'animalBaseF.png', 'animalBaseG.png', 'animalBaseH.png', 'animalBaseI.png', 'animalBaseJ.png', 'animalC.png', 'animalD.png', 'animalE.png', 'animalF.png', 'animalG.png', 'animalH.png', 'animalI.png', 'animalJ.png', 'astroFemaleA.png', 'astroFemaleB.png', 'astroMaleA.png', 'astroMaleB.png', 'athleteFemaleBlue.png', 'athleteFemaleGreen.png', 'athleteFemaleRed.png', 'athleteFemaleYellow.png', 'athleteMaleBlue.png', 'athleteMaleGreen.png', 'athleteMaleRed.png', 'athleteMaleYellow.png', 'businessMaleA.png', 'businessMaleB.png', 'casualFemaleA.png', 'casualFemaleB.png', 'casualMaleA.png', 'casualMaleB.png', 'cyborg.png', 'fantasyFemaleA.png', 'fantasyFemaleB.png', 'fantasyMaleA.png', 'fantasyMaleB.png', 'farmerA.png', 'farmerB.png', 'militaryFemaleA.png', 'militaryFemaleB.png', 'militaryMaleA.png', 'militaryMaleB.png', 'racerBlueFemale.png', 'racerBlueMale.png', 'racerGreenFemale.png', 'racerGreenMale.png', 'racerOrangeFemale.png', 'racerOrangeMale.png', 'racerPurpleFemale.png', 'racerPurpleMale.png', 'racerRedFemale.png', 'racerRedMale.png', 'robot.png', 'robot2.png', 'robot3.png', 'survivorFemaleA.png', 'survivorFemaleB.png', 'survivorMaleA.png', 'survivorMaleB.png', 'zombieA.png', 'zombieB.png', 'zombieC.png'];
let skin_directory = "assets/skins/";

let playerSkins = {};
skin_files.forEach(file => {
    let map = texLoader.load(skin_directory + file);
    map.encoding = THREE.sRGBEncoding;
    map.flipY = false;
    playerSkins[file.split(".")[0]] = map;
});

///////////// CHARACTER & ANIMATIONS /////////////

const asset_url = "assets/characterMediumAllAnimations.glb"; 

// Animations in gltf.animations that need to be looped
const loopedAnimations = ["CrouchIdle", "CrouchWalk", "Idle", "RacingIdle", "Run", "Walk", "Jump"]

interface AnimationInfo {
    animation : THREE.AnimationClip,
    loop : boolean,
}

const gltfLoader = new GLTFLoader(manager);
gltfLoader.load(asset_url, ( gltf ) => {

    Player.gltf = gltf;

    gltf.animations.forEach(anim => {

        let animInfo : AnimationInfo = {
            animation : anim,
            loop : loopedAnimations.includes(anim.name),
        };

        Player.animations[anim.name] = animInfo;

    });

});

for (var accessory in Accessories) {
    let url = `assets/accessories/${accessory}.glb`
    gltfLoader.load(url, (gltf) => {
        let filename = url.split("/").pop();
        let accessoryName = filename.split(".")[0];
        Accessories[accessoryName].scene = gltf.scene;
    });
}
manager.onLoad = () => {
    Player.accessories = Accessories;
    Player.skins = playerSkins;
}

///////////////////////////////////////////// LIGHTING /////////////////////////////////////////////

// Ambient Light
const ambientColor = 0xFFFFFF;
const ambiIntensity = 0.8;
const ambilight = new THREE.AmbientLight(ambientColor, ambiIntensity);
ambilight.visible = true;
scene.add(ambilight);

// Directional light
const dirColor = 0xffffbb;
const dirIntensity = 2.0;
const dirlight = new THREE.DirectionalLight(dirColor, dirIntensity);
dirlight.position.set(0, 10, 0);
dirlight.target.position.set(2, 4, 6);
scene.add(dirlight);
scene.add(dirlight.target);
const helper = new THREE.DirectionalLightHelper(dirlight);
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


///////////////////////////////////////// COMMAND HANDLING /////////////////////////////////////////

function onMessageArrived(message : any) {
    console.log("onMessageArrived: "+message.payloadString);   
    commandHandler(message.destinationName, message.payloadString);
}

const _cmdStringAddPlayer = "add";
const _cmdStringRemovePlayer = "remove";
const _cmdStringChangeSkin = "skin";
const _cmdStringChangeAnimation = "animation";
const _cmdStringSay = "say";
const _cmdStringChangeAccessory = "accessory";
const _cmdStringAssignTeam = "team";
const _cmdStringSplitTeams = "split";

function playerCommandHandler(command: string[], playerID: string) {
    if (playerID === "" || playerID === undefined) {
        switch (command[0]) {
            case _cmdStringChangeSkin:
            case _cmdStringChangeAnimation:
            case _cmdStringChangeAccessory:
            case _cmdStringSay:
            case _cmdStringAssignTeam:
                for (let playerName in playerManager.players) {
                    playerCommandHandler(command, playerName);
                }
                break;
            
            default:
                console.warn(`${command} was not a recognized command on this topic`);
                break;
        }
    }

    switch (command[0]) {
        case _cmdStringAddPlayer:
            playerManager.addPlayer(playerID);
            break;
        
        case _cmdStringRemovePlayer:
            playerManager.removePlayer(playerID);
            break;

        case _cmdStringChangeSkin:
            playerManager.players[playerID].skin = command[1];
            break;

        case _cmdStringChangeAnimation:
            playerManager.players[playerID].changeAnimation(command[1]);
            break;

        case _cmdStringSay:
            playerManager.players[playerID].say(command.slice(1).join(" "));
            break;

        case _cmdStringChangeAccessory:
            playerManager.players[playerID].accessory = command[1];
            break;

        case _cmdStringAssignTeam:
            playerManager.assignTeam(playerID, command[1]);
            break;
        
        default:
            console.warn(`${command} was not a recognized command`)
            break;
    }
}

function teamCommandHandler(command: string[], teamID: string) {

    switch (command[0]) {

        case _cmdStringChangeSkin:
        case _cmdStringChangeAnimation:
        case _cmdStringSay:
        case _cmdStringChangeAccessory:
        case _cmdStringAssignTeam:
            // Run command for every player in team
            if (!(teamID in playerManager.teams)) {
                console.warn(`Team "${teamID}" does not exist`);
            } else {
                playerManager.teams[teamID].players.forEach( (player) => {
                    playerCommandHandler(command, player.id);
                });
            }         
            break;
    
        case _cmdStringSplitTeams:
            let teamNames = command.splice(1);   
            let i = 0;
            let tot = Object.keys(playerManager.players).length;
            for (let playerName in playerManager.players) {
                playerManager.assignTeam(playerName, teamNames[Math.floor(i/tot * teamNames.length)]);
                i++;
            }
            break;

        case "reset":
            // If teamID is not specified, reset all teams
            if (teamID) {

                if (!(teamID in playerManager.teams)) {
                    console.warn(`Team "${teamID}" does not exist`);
                } else {
                    playerManager.teams[teamID].players.forEach(player => {
                        playerManager.assignTeam(player.id, playerManager.defaultTeam.name);
                    });
                }

            } else {
                for (let playerName in playerManager.players) {
                    playerManager.assignTeam(playerName, playerManager.defaultTeam.name);
                }
            }
            break;

        default:
            break;
    }
}

function billboardCommandHandler(command: string[]) {
    switch (command[0]) {
        case "show":
            if (command[1]) {
                billboard.setBase64Image(command.splice(1).join(','));
            } else {
                billboard.mesh.visible = true;
            }
            break;
        
        case 'hide':
            billboard.mesh.visible = false;
            break

        default:
            break;
    }
}

function commandHandler(topic, msg) {
    let command_topic = topic.split("/");
    let command = msg.split(",");

    switch (command_topic[0]) {
        case "players":
            playerCommandHandler(command, command_topic[1]);
            break;

        case "teams":
            teamCommandHandler(command, command_topic[1]);
            break;
        
        case "billboard":
            billboardCommandHandler(command);
            break;

        default:
            console.warn(`Unrecognized topic ${topic} for command ${msg}`)
            break;
    }   
}

function onMQTTConnect() {
    console.log("Connected to " + mqttclient.uri);
    mqttclient.subscribe("players/#");
    mqttclient.subscribe("teams/#");
    mqttclient.subscribe("billboard/#");
    subButton.disabled = false;
    pubButton.disabled = false;
}

function onMQTTConnectionLost(response) {
    if (response.errorCode !== 0) {
        console.error("Connection lost: " + response.errorMessage);
        subButton.disabled = true;
        subButton.disabled = true;
    }
}

function _btnPublish() {
    let topic = (<HTMLInputElement>document.getElementById("pub-topic")).value;
    let payload = (<HTMLInputElement>document.getElementById("pub-payload")).value;
    mqttclient.publish(topic, payload);
}

function _btnSubscribe() {
    let topic = (<HTMLInputElement>document.getElementById("sub-topic")).value;
    mqttclient.subscribe(topic);
}