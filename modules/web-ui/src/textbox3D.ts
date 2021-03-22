import { Vector3 } from "three";
import { UpdateObject } from "./updateObject";

export class TextBox3D extends UpdateObject {
    static canvas: HTMLCanvasElement;

    position: Vector3;
    textElement: HTMLDivElement;
    textOffsetWidth: number;
    textOffsetHeight: number;
    hasTriangle: boolean;
    triangleElement: HTMLDivElement;
    triangleSize = 10;
    color = '#FFFFFF88';

    private _visible: boolean = true;

    constructor (text: string, position: Vector3, hasTriangle?: boolean) {
        super();
        this.position = position;
        TextBox3D.canvas = UpdateObject.context.renderer.domElement;

    
        this.textElement = document.createElement('div');
        this.textElement.style.position = 'absolute';
        this.textElement.style.width = 'fit-content';
        this.textElement.style.height = 'fit-content';
        this.textElement.style.paddingLeft = '10px';
        this.textElement.style.paddingRight = '10px';
        this.textElement.style.fontSize = '18px';
        this.textElement.style.backgroundColor = this.color;
        this.textElement.style.borderRadius = '10px';
        this.textElement.innerHTML = text;
        document.body.appendChild(this.textElement);
        this.textOffsetWidth = this.textElement.offsetWidth;
        this.textOffsetHeight = this.textElement.offsetHeight;

        this.hasTriangle = hasTriangle || false;
        if (this.hasTriangle) {
            this.triangleElement = document.createElement('div');
            this.triangleElement.style.position = 'absolute';
            this.triangleElement.style.width = '0';
            this.triangleElement.style.height = '0';
            this.triangleElement.style.borderLeft = this.triangleSize + 'px solid transparent';
            this.triangleElement.style.borderRight = this.triangleSize + 'px solid transparent';
            this.triangleElement.style.borderTop = this.triangleSize * 1.5 + 'px solid ' +  this.color;
            document.body.appendChild(this.triangleElement);
        }
    }


    update(delta : number) {
        if (!this._visible) { return; }
        var position2D = new Vector3().copy(this.position);
        // map to normalized device coordinate (NDC) space
        position2D.project( UpdateObject.context.camera );

        // map to 2D screen space
        position2D.x = Math.round( (   position2D.x + 1 ) * TextBox3D.canvas.width  / 2 );
        position2D.y = Math.round( ( - position2D.y + 1 ) * TextBox3D.canvas.height / 2 );
    
        var elemCoords = {
            x: position2D.x - this.textOffsetWidth / 2,
            y: position2D.y - this.textOffsetHeight /2
        }
        this.textElement.style.left = elemCoords.x + 'px';
        this.textElement.style.top = elemCoords.y + 'px';

        if (this.hasTriangle) {
            this.triangleElement.style.left = elemCoords.x + (this.textOffsetWidth / 2 - this.triangleSize) + 'px';
            this.triangleElement.style.top = elemCoords.y + (this.textOffsetHeight) + 'px';
        }
        // TODO change fontSize & triangleSize based on distance to camera
        // TODO change zindex based on depth (minor)
    }

    set visible(val: boolean) {
        if (this._visible !== val) {
            this._visible = val;
            if (val) {
                document.body.appendChild(this.textElement);
            } else {
                document.body.removeChild(this.textElement);
            }
        }
    }

    get visible() {
        return this._visible;
    }

    destroy() {
        if (this.textElement) { this.textElement.remove(); }
        if (this.triangleElement) { this.triangleElement.remove(); }
        super.destroy();
    }
}