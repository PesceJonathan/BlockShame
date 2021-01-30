import {spawn} from 'child_process'
import path from 'path'
import {io, Socket} from 'socket.io-client'

export function startProgram(){
    let python = spawn('python', ['../VirtualWebcam/VirtualWebcam.py']);
    python.stdout.on('data', (data) => {
        console.log(`stdout: ${data}`);
    });
    
    python.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
    });
    
    python.on('close', (code) => {
        console.log(`child process exited with code ${code}`);
    });
}

let socket : null | Socket = null;
export function connect(): Promise<void>{
    return new Promise((res, rej) => {
        socket = io('http://localhost:5000');
        // if(socket != null){
        //     socket.onopen = (ev: Event) => {
        //         res();
        //     }
        // }
        socket.on('connect', ()=> {
            console.log("HI");
            res();
        })
    })
}

export function sendMessage(obj: any) {
    if(socket){
        socket.emit("setting_change", obj);
    }
}