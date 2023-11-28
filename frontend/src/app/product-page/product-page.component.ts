import { Component } from '@angular/core';
import { StoreService } from '../store.service';
import { SingleProduct, SingleProductState, LoadingState } from '../store/types';
import { Observable, map } from 'rxjs';
import { skipWhile } from 'rxjs';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-product-page',
  templateUrl: './product-page.component.html',
  styleUrls: ['./product-page.component.scss'],
  host: {class: 'p-4 w-full h-full overflow-scroll'}
})
export class ProductPageComponent {
  public productState$: Observable<SingleProductState>;
  public isProductLoaded$: Observable<Boolean>;
  private productId: string | null;

  constructor(private store: StoreService, private route: ActivatedRoute) {
    this.productState$ = this.store.single_product_state$;
    this.isProductLoaded$ = this.productState$.pipe(map((productState : SingleProductState) => productState.state == LoadingState.Loaded));
    this.productId = this.route.snapshot.paramMap.get('productId');
    this.store.getProduct(this.productId);
  }
}
