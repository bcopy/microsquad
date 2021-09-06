import { AnimationMixer, Bone, Group, LoopOnce, Material, Mesh,  Object3D, Vector3 } from 'three';
import { GLTF } from 'three/examples/jsm/loaders/GLTFLoader';
import { TextBox3D } from './textbox3D';
import { UpdateObject } from './updateObject';
import { SkeletonUtils } from 'three/examples/jsm/utils/SkeletonUtils'
import { DialogBox3D } from './dialogbox3D';
import { Team } from './team';


export class Player extends UpdateObject {
    static gltf : GLTF;
    static animations = {};
    static model_scale = 0.7;
    static nametag_height = 4.8;
    static dialog_height = 4.8;
    static accessories;
    static skins = {};

    id : string;
    order: number;
    team : Team;
    model : Object3D;
    model_loaded : boolean = false;
    mixer : AnimationMixer;
    nametag : TextBox3D;
    dialog_box : DialogBox3D;
    private _skin : string;
    private _accessory : string;

    constructor (id : string, team: Team, order : number = 0) {
        super();
        this.id = id;
        this.team = team;
        this.order = order;
        team.addPlayer(this);

        this.nametag = new TextBox3D(id, new Vector3(0, 0, 0));
        this.nametag.visible = false;

        if (Player.gltf) {
            this.setModel();
        }
    }

    private setModel() {
        this.model_loaded = true;
        this.model = SkeletonUtils.clone(Player.gltf.scene);
        this.model.scale.set( Player.model_scale, Player.model_scale, Player.model_scale );
        UpdateObject.context.scene.add( this.model );
        
        // Set random skin
        let skins_names = Object.keys(Player.skins);
        let random_skin = skins_names[skins_names.length * Math.random() << 0];
        this.skin = random_skin;

        this.mixer = new AnimationMixer( this.model );

        this.changeAnimation("Idle");
    }

    changeAnimation(name: string) {
        if (name in Player.animations) {
            let animInfo = Player.animations[name];
            this.mixer.stopAllAction();
            var action = this.mixer.clipAction(animInfo.animation);
            if (!animInfo.loop) { 
                action.setLoop(LoopOnce, 1); 
                action.clampWhenFinished = true;
            }
            action.play();
        } else {
            console.warn(`Animation "${name}" not found!`);
        }     
    }

    changeTeam(team: Team) {
        this.team.removePlayer(this);
        this.team = team;
        team.addPlayer(this);
    }
    
    say(message: string) {
        if (this.dialog_box) {
            this.dialog_box.destroy();
        }
        let p = this.position.clone();
        p.y += Player.dialog_height * this.scale;
        this.dialog_box = new DialogBox3D(message, p, 3);
    }

    set accessory(name: string) {
        if (name in Player.accessories) {
            let accessory = Player.accessories[name];

            // Remove old accessory
            if (this._accessory) {
                this.model.traverse( (object) => {
                    if (object instanceof Group && object.name === this._accessory) {
                        object.parent.remove(object);
                    }
                });
            }
            
    
            this.model.traverse( (object) => {
                if ( object instanceof Bone && object.name === accessory.bone) {
                    let sc = accessory.scene.clone();
                    sc.name = name;
                    sc.position.x = accessory.position.x;
                    sc.position.y = accessory.position.y;
                    sc.position.z = accessory.position.z;
                    object.add(sc);
                }
            });
            this._accessory = name;

        } else {
            console.warn(`Accessory "${name}" not found!`)
        }
    }

    get accessory() {
        return this._accessory;
    }

    set skin(name: string) {
        if (name in Player.skins) {
            var mat; // https://discourse.threejs.org/t/giving-a-glb-a-texture-in-code/15071/6

            this.model.traverse( (object) => {
    
                if ( object instanceof Mesh ) {
                    mat = (<Material>object.material).clone();
                    mat.map = Player.skins[name];
                    mat.roughness = 0.85;
                    mat.needsUpdate = true;
                    object.material = mat;
                } 
             
            });
            this._skin = name;
        } else {
            console.warn(`Skin "${name}" not found!`);
        }
    }

    get skin() {
        return this._skin;
    }

    set rotation(val: Vector3) {
        if (this.model) {
            this.model.rotation.set(val.x, val.y, val.z);
        }
    }

    get rotation() {
        return this.model.rotation.toVector3();
    }

    set position(val: Vector3) {
        if (this.model) {
            this.model.position.set(val.x, val.y, val.z);
            this.nametag.position.copy(this.model.position).y += Player.nametag_height * this.scale;
        }
    }

    get position() {
        return this.model.position;
    }

    set scale(val : number) {
        if (this.model) {
            this.model.scale.set(val, val, val);
            this.nametag.position.copy(this.model.position).y += Player.nametag_height * this.scale;
        }
    }

    get scale() {
        return this.model.scale.x;
    }

    update(delta : number) {
        if (this.mixer) { this.mixer.update( delta ) }
        if (!this.model_loaded && Player.gltf) { this.setModel() }
    }

    destroy() {
        this.team.removePlayer(this);

        UpdateObject.context.scene.remove( this.model );

        this.model.traverse((object) => {
            let obj = <any> object;
            if (obj.geometry !== undefined) {
                obj.geometry.dispose();
                obj.material.dispose();
            }
        });    
    }
}