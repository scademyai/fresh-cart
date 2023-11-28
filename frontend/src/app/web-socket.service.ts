import { Injectable } from '@angular/core';
import { map } from 'rxjs';
import { Socket } from 'ngx-socket-io';

export interface SocketResponse {
  text?: string;
  json?: any;
  cart?: any;
}

@Injectable({
  providedIn: 'root'
})
export class SocketService {
  constructor(private socket: Socket) {}

  sendMessage(type: string, message: string) {
    const token = localStorage.getItem('token')
    this.socket.emit(type, {"text": message, "token": token});
  }

  getMessage(type: string) {
    return this.socket.fromEvent(type).pipe(map((data:any) => data));
  }
}
