import { Component, OnChanges, OnInit, SimpleChanges } from '@angular/core';
import { UntilDestroy } from '@ngneat/until-destroy';
import { map, skipWhile } from 'rxjs';
import { Observable } from 'rxjs/internal/Observable';
import { AppService } from '../app.service';
import { StoreService } from '../store.service';
import { CartData, CartState, Product, ProductState } from '../store/types';
import { SocketService } from '../web-socket.service';

@UntilDestroy()
@Component({
  selector: 'app-cart',
  templateUrl: './cart.component.html',
  styleUrls: ['./cart.component.scss']
})
export class CartComponent implements OnInit {
  public items: string[] = [
    "First",
    "Second",
    "Third"
  ];
  public readonly products$: Observable<Product[] | undefined>;
  public total$: Observable<number>;
  

  constructor(public socket: SocketService, public store: StoreService, private appService: AppService) {
    this.products$ = this.store.cart$.pipe(
      skipWhile((state: CartState) => !state.data.cart),
      map((state: CartState) => {
        return state.data.cart
      }),
    );
  }
  
  ngOnInit(): void {
   this.total$ = this.products$.pipe(
      map((products: Product[] | undefined) => {
        if (products) {
          return products.reduce((total, product) => total + product.price * product.quantity, 0);
        }
   
        return 0;
      })
    );
  }

  addProduct(product: Product) {
    this.store.addToCart(product);
  }

  deleteCart() {
    this.store.deleteCart().subscribe((cartData: CartData) => {
      this.store.setCart(cartData);
    });
  }

  deleteProduct(productId: number) {
    this.store.deleteProduct(productId).subscribe((cartData: CartData) => {
      this.store.setCart(cartData);
    })
  }
}
