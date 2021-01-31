import { spawn } from "child_process";
import {resolve} from "path";
import { io, Socket } from "socket.io-client";

export function startProgram(scriptPath: string, callback: (code: number) => void) {
  let python = spawn(`python`, [scriptPath] );
  python.stdout.on("data", (data) => {
    console.log(`stdout: ${data}`);
  });

  python.stderr.on("data", (data) => {
    console.error(`stderr: ${data}`);
  });

  python.on("close", (code) => {
    console.log(`child process exited with code ${code}`);
  });

  python.on("exit", (code: number) => {
    console.log("Process quit with code : " + code);
    callback(code);
  });
}

let socket: null | Socket = null;
export function connect(): Promise<void> {
  return new Promise((res, rej) => {
    socket = io("http://localhost:5000");
    // if(socket != null){
    //     socket.onopen = (ev: Event) => {
    //         res();
    //     }
    // }
    socket.on("connect", () => {
      console.log("HI");
      res();
    });
  });
}

export function sendMessage(obj: any, event = "setting_change") {
  if (socket) {
    socket.emit(event, obj);
  }
}
