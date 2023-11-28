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
import { StoreService, defaultProductState } from '../store.service';
import { CartState, LoadingState, Product } from '../store/types';
import { EMPTY } from 'rxjs';
import { TestScheduler } from 'rxjs/testing';

describe('CartComponent', () => {
  let component: CartComponent;
  let fixture: ComponentFixture<CartComponent>;
  let testScheduler: TestScheduler;
  const store: any = { state$: EMPTY, cart$: EMPTY };
  const cart: CartState = { state: LoadingState.Loaded, data: { cart: [{id: 1, name: 'apple', quantity: 2, price:3.2}] } };

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CartComponent ],
      imports: [SocketIoModule.forRoot(config), MatFormFieldModule, MarkdownModule.forRoot(), ReactiveFormsModule, MatListModule, MatInputModule, BrowserAnimationsModule, HttpClientTestingModule],
      providers: [
        SocketService,
        {
          provide: StoreService,
          useValue: store,
        }
      ]
    })
    .compileComponents();

    testScheduler = new TestScheduler((actual, expected) => {
      expect(actual).toEqual(expected);
    });
    fixture = TestBed.createComponent(CartComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should load products', () => {
    testScheduler.run((helpers) => {
      const { expectObservable, cold } = helpers;
      store.cart$ = cold('a', { a: cart });
      const expected = cold('a', { a: cart.data.cart });
      fixture = TestBed.createComponent(CartComponent);

      expectObservable(fixture.componentInstance.products$).toEqual(
        expected
      );
    });
  });
});
