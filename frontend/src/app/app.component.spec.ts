import { TestBed } from '@angular/core/testing';
import { MatIconModule } from '@angular/material/icon';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatToolbarModule } from '@angular/material/toolbar';
import { RouterTestingModule } from '@angular/router/testing';
import { AppComponent } from './app.component';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { MatGridListModule } from '@angular/material/grid-list';
import { ChatComponent } from './chat/chat.component';
import { Socket } from 'ngx-socket-io';
import { SocketService } from './web-socket.service';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { MarkdownModule } from 'ngx-markdown';
import { MatFormFieldModule } from '@angular/material/form-field';

describe('AppComponent', () => {
  const socketSpy = jasmine.createSpyObj('Socket', ['fromEvent', 'emit']);
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        RouterTestingModule,
        MatToolbarModule,
        MatIconModule,
        MatPaginatorModule,
        HttpClientTestingModule,
        MatGridListModule,
        MatSnackBarModule,
        MarkdownModule.forRoot(),
        MatFormFieldModule,
      ],
      providers: [
        SocketService,
        {provide: Socket, useValue: socketSpy}
      ],
      declarations: [
        AppComponent,
        ChatComponent
      ],
    }).compileComponents();
  });

  it('should create the app', () => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.componentInstance;
    expect(app).toBeTruthy();
  });

  it(`should have as title 'client'`, () => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.componentInstance;
    expect(app.title).toEqual('client');
  });

});
