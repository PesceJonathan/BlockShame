import {spawn} from 'child_process'
import path from 'path'

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