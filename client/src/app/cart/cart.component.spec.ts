import { ComponentFixture, TestBed } from '@angular/core/testing';
import { SocketService } from '../web-socket.service';
import { config } from '../app.module'
import { CartComponent } from './cart.component';
import { SocketIoModule } from 'ngx-socket-io';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MarkdownModule } from 'ngx-markdown';
import { ReactiveFormsModule } from '@angular/forms';
import { MatListModule } from '@angular/material/list';
import { MatInputModule } from '@angular/material/input';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HttpClientTestingModule } from '@angular/common/http/testing';

describe('CartComponent', () => {
  let component: CartComponent;
  let fixture: ComponentFixture<CartComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CartComponent ],
      imports: [SocketIoModule.forRoot(config), MatFormFieldModule, MarkdownModule.forRoot(), ReactiveFormsModule, MatListModule, MatInputModule, BrowserAnimationsModule, HttpClientTestingModule],
      providers: [ SocketService ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CartComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
