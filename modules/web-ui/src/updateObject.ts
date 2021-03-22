import { Camera, Renderer, Scene } from "three";

export interface Context {
    scene : Scene;
    camera: Camera;
    renderer: Renderer;
    objList : UpdateObject[];
}

export abstract class UpdateObject {
    static context : Context;
    
    constructor () {
        UpdateObject.context.objList.push(this);
    }

    abstract update(delta : number): void;

    destroy() {
        var index = UpdateObject.context.objList.indexOf(this);
        if (index !== -1) {
            UpdateObject.context.objList.splice(index, 1);
        }
    }
}