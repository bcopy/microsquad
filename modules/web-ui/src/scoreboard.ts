import * as THREE from "three";
import { Context } from "./updateObject";
import { MqttMicrosquadEventType, MqttUpdateEvent } from "./mqtt";
import { Observable } from "rxjs";

export class Scoreboard {
    mesh: THREE.Mesh;
    context: Context;
    geometry: THREE.PlaneGeometry;
    material: THREE.MeshBasicMaterial;
    height = 4.5;
    position = new THREE.Vector3(0, 5, 10);
    rotation = new THREE.Euler(0, Math.PI, 0);

    constructor(context: Context, observable: Observable<MqttUpdateEvent>) {
        this.context = context;
        observable.subscribe(this.observer);
    }

    observer = {
        next: (event) => {this.handleMQTTUpdateEvent(event)},
        error: err => console.log("Error handling MQTT Update Event "+err)
    }

    handleMQTTUpdateEvent(event : MqttUpdateEvent){
        if(event.type === MqttMicrosquadEventType.SCOREBOARD_UPDATE){
            switch(event.property){
                case "show":
                    if(this.mesh){
                      this.mesh.visible = Boolean(event.newValue).valueOf();
                    }
                    break;
                case "image":
                    this.setBase64Image(event.newValue);
                    break;
                case "score":
                    // TODO: Superimpose score over image, if not empty
                    break;
                default:
                    console.log("Unhandled scoreboard property :"+event.property);
            }
        }

    }

    setBase64Image(base64Image: string) {
        // Dispose existing resources
        if (this.mesh) {
            this.context.scene.remove( this.mesh );
        }
        if (this.geometry) {
            this.geometry.dispose();
        }
        if (this.material) {
            this.material.dispose();
        }

        // Generate image element from b64
        let image: HTMLImageElement = new Image();
        image.src = base64Image;
        let texture = new THREE.Texture();
        texture.image = image;

        image.onload = () => {
            texture.needsUpdate = true;

            texture.wrapS = texture.wrapT = THREE.MirroredRepeatWrapping;

            // Create mesh
            this.geometry = new THREE.PlaneGeometry(this.height * image.width / image.height, this.height);
            this.material = new THREE.MeshBasicMaterial({
                map: texture,
                transparent: true
            });
            this.mesh = new THREE.Mesh(this.geometry, this.material);
            this.mesh.visible = true;

            this.mesh.position.copy(this.position);
            this.mesh.rotation.copy(this.rotation);
            this.context.scene.add(this.mesh);
        };
    }
}
