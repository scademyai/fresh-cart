import { TestBed } from '@angular/core/testing';
import { SocketIoModule } from 'ngx-socket-io';
import { config } from './app.module'
import { SocketService } from './web-socket.service';
import { Socket } from 'ngx-socket-io';
import { of } from 'rxjs';

describe('WebSocketService', () => {
  let service: SocketService;
  const socketSpy = jasmine.createSpyObj('Socket', ['fromEvent', 'emit']);
  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [SocketIoModule.forRoot(config)],
      providers: [
        SocketService,
        {provide: Socket, useValue: socketSpy}
      ]
    });
    service = TestBed.inject(SocketService);
  });

  beforeEach(() => {
    localStorage.clear();
    localStorage.setItem('token', 'testToken');
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should emit message with the correct arguments', () => {
    const type = 'testType';
    const message = 'testMessage';
    const token = localStorage.getItem('token');
  
    service.sendMessage(type, message);
  
    expect(socketSpy.emit).toHaveBeenCalledWith(type, { text: message, token: token});
  });

  it('should return an observable with the correct data', (done) => {
    const type = 'testType';
    const testData = { message: 'test message' };
    const fromEventSpy = socketSpy.fromEvent.and.returnValue(of(testData));
  
    service.getMessage(type).subscribe((data) => {
      expect(data).toEqual(testData);
      expect(fromEventSpy).toHaveBeenCalledWith(type);
      done();
    });
  });

});
