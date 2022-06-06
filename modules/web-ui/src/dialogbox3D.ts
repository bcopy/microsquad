import { Vector3 } from "three";
import { TextBox3D } from "./textbox3D"

export class DialogBox3D extends TextBox3D {
    timeout: number;
    elapsedTime: number = 0;
    constructor(text: string, position: Vector3, timeout: number) {
        super(text, position, true);
        this.timeout = timeout;
    }

    update(delta: number) {
        super.update(delta);
        this.elapsedTime += delta;
        if (this.elapsedTime > this.timeout) {
            this.destroy();
        }
    }
}