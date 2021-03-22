import * as THREE from "three";
import { Context } from "./updateObject";

export class Billboard {
    mesh: THREE.Mesh;
    
    constructor(context: Context) {
        let image: HTMLImageElement = new Image();
        image.src = '';
        let texture = new THREE.Texture();
        texture.image = image;
        image.onload = () => {
            texture.needsUpdate = true;
        };
        texture.wrapS = texture.wrapT = THREE.MirroredRepeatWrapping;
        const billboardGeometry = new THREE.PlaneGeometry(8,4.5, 1, 1);
        const billboardMaterial = new THREE.MeshBasicMaterial( {
            map: texture
        });
        this.mesh = new THREE.Mesh( billboardGeometry, billboardMaterial );
        this.mesh.position.set(0, 4, 10);
        this.mesh.rotation.set(0, Math.PI, 0);
        this.mesh.visible = false;
        context.scene.add( this.mesh );

        texture.dispose();
    }

    setBase64Image(base64Image: string) {
        let image: HTMLImageElement = new Image();
        image.src = base64Image;
        let texture = new THREE.Texture();
        texture.image = image;
        image.onload = () => {
            texture.needsUpdate = true;
            this.mesh.visible = true;
        };
        texture.wrapS = texture.wrapT = THREE.MirroredRepeatWrapping;

        var mat; // https://discourse.threejs.org/t/giving-a-glb-a-texture-in-code/15071/6

        this.mesh.traverse( (object) => {

            if ( object instanceof THREE.Mesh ) {
                mat = (<THREE.Material>object.material).clone();
                mat.map = texture;
                mat.needsUpdate = true;
                object.material = mat;
            } 
            
        });
    }
}
