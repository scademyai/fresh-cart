import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { routes } from '../app-routing.module';
import { RouterTestingModule } from '@angular/router/testing';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { ShopComponent } from './shop.component';
import { Socket } from 'ngx-socket-io';
import { MatFormFieldControl, MatFormFieldModule } from '@angular/material/form-field';
import { SocketService } from '../web-socket.service';
import { MatIconModule } from '@angular/material/icon';
import { MatPaginatorModule } from '@angular/material/paginator';
import { ReactiveFormsModule } from '@angular/forms';
import { MatInputModule } from '@angular/material/input';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

describe('ShopComponent', () => {
  let component: ShopComponent;
  let fixture: ComponentFixture<ShopComponent>;
  const socketSpy = jasmine.createSpyObj('Socket', ['fromEvent', 'emit']);

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ 
        HttpClientTestingModule, 
        MatPaginatorModule, 
        MatFormFieldModule, 
        MatIconModule, 
        RouterTestingModule.withRoutes(routes), 
        MatSnackBarModule, 
        ReactiveFormsModule,
        MatInputModule,
        BrowserAnimationsModule
      ],
      providers: [
        SocketService,
        {provide: Socket, useValue: socketSpy}
      ],
      declarations: [ ShopComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ShopComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
