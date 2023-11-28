import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, catchError, EMPTY, map, Observable } from 'rxjs';
import { CartData, CartState, Product, SingleProduct, SingleProductState } from './store/types';
import { LoadingState, ProductState } from './store/types';
import { HttpService } from './http.service';


export const defaultProductState: ProductState = {
  state: LoadingState.Loading,
  data: []
};

export const defaultSingleProductState: SingleProductState = {
  state: LoadingState.Loading
};

export const defaultCartState: CartState = {
  state: LoadingState.Loading,
  data: {
    cart: []
  }
}

@Injectable({
  providedIn: 'root'
})
export class StoreService {
  private _state$: BehaviorSubject<ProductState> =
    new BehaviorSubject<ProductState>(defaultProductState);
  private _single_product_state$: BehaviorSubject<SingleProductState> =
    new BehaviorSubject<SingleProductState>(defaultSingleProductState);
  public readonly state$: Observable<ProductState> = this._state$.asObservable();
  public readonly single_product_state$: Observable<SingleProductState> = this._single_product_state$.asObservable();

  private _cart$: BehaviorSubject<CartState> = new BehaviorSubject<CartState>(defaultCartState);
  public readonly cart$: Observable<CartState> = this._cart$.asObservable();

  constructor(private httpClient: HttpClient, private http: HttpService) { }

  refresh() {
    this.http
      .get<Product[]>('/api/products')
      .pipe(
        catchError(() => EMPTY),
        map(this.toState)
      )
      .subscribe((state: ProductState) => this._state$.next(state));
  }

  private toState(response: Product[]): ProductState {
    return {
      state: LoadingState.Loaded,
      data: response
    };
  }

  private toSingleProductState(response: SingleProduct): SingleProductState {
    return {
      state: LoadingState.Loaded,
      data: response
    };
  }

  private toCartState(response: CartData): CartState {
    return {
      state: LoadingState.Loaded,
      data: {
        cart: response.cart
      }
    };
  }

  addToCart(product: Product) {
    this.http.post<CartData>('/api/cart', {"product": product}).subscribe(
      (data: CartData) => this.setCart(data),
      );
  }

  getCart() {
    this.http.get<CartData>('/api/cart')
    .pipe(
      catchError(() => EMPTY),
      map(this.toCartState)
    )
    .subscribe((cart: CartState)=> this._cart$.next(cart))
  }

  setCart(cartData: CartData) {

    this._cart$.next({
      state: LoadingState.Loaded,
      data: cartData
    })
  }

  deleteCart(): Observable<any> {
    return this.http.delete('/api/cart')
  }

  deleteProduct(productId: number): Observable<CartData> {
    return this.http.delete<CartData>(`/api/cart/${productId}`)
  }

  getProduct(productId: string | null) {
    this._single_product_state$.next(defaultSingleProductState)
    return this.http.get<SingleProduct>(`/api/products/${productId}`)
    .pipe(
      catchError(() => EMPTY),
      map(this.toSingleProductState)
    )
    .subscribe((state: SingleProductState) => this._single_product_state$.next(state));
  }
}
