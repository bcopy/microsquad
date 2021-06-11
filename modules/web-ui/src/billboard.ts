import * as THREE from "three";
import { Context } from "./updateObject";

export class Billboard {
    mesh: THREE.Mesh;
    context: Context;
    geometry: THREE.PlaneGeometry;
    material: THREE.MeshBasicMaterial;
    height = 4.5;
    position = new THREE.Vector3(0, 5, 10);
    rotation = new THREE.Euler(0, Math.PI, 0);

    constructor(context: Context) {
        this.context = context;
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
