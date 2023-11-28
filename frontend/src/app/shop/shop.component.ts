import { Component, OnInit, OnDestroy, ViewChild } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { UntilDestroy, untilDestroyed } from '@ngneat/until-destroy';
import { Observable, BehaviorSubject, map } from 'rxjs';
import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';
import { StoreService } from '../store.service';
import { skipWhile } from 'rxjs';
import { Product, ProductState } from '../store/types';
import { ActivatedRoute } from '@angular/router';
import { MatSnackBar, MatSnackBarConfig } from '@angular/material/snack-bar';
import { FormGroup, FormControl } from '@angular/forms';
import { SocketService } from '../web-socket.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-shop',
  templateUrl: './shop.component.html',
  styleUrls: ['./shop.component.scss'],
  host: {class: 'p-4 w-full h-full overflow-scroll'}
})
export class ShopComponent implements OnInit, OnDestroy {
  public readonly products$: Observable<Product[] | undefined>;
  dataSource: MatTableDataSource<Product>;
  obs: Observable<Product[] | undefined>;
  
  searchForm = new FormGroup({
    searchInput: new FormControl('')
  })
  @ViewChild(MatPaginator) paginator: MatPaginator;

  constructor(private store: StoreService, private route: ActivatedRoute, private snackBar: MatSnackBar, public socket: SocketService, private router: Router) {
    this.products$ = this.store.state$.pipe(
      skipWhile((state: ProductState) => !state.data),
      map((state: ProductState) => {return this.getDataTableSource(state.data)}),
    );

    this.route.queryParamMap.subscribe(paramMap => {
      const filterValue = paramMap.get('products');
  
      if (filterValue && this.dataSource) {
        this.applyFilter(filterValue);
      }
    })
  }

  ngOnInit() {
   this.products$.subscribe()
   this.searchForm.valueChanges.subscribe((value: any) => this.search())
  }

  ngOnDestroy(): void {
    if (this.dataSource)
      this.dataSource.disconnect();
  }

  getDataTableSource(products: Product[]) {
    this.dataSource = new MatTableDataSource(products);
    this.dataSource.paginator = this.paginator;
    this.obs = this.dataSource.connect();

    this.route.queryParamMap.subscribe(paramMap => {
      const filterValue = paramMap.get('products');
  
      if (filterValue && this.dataSource) {
        this.applyFilter(filterValue);
      }
    })
  
    return products;
  }

  private applyFilter(filterValue: string) {
    this.dataSource.filter = filterValue.trim().toLowerCase();
  
    if (this.dataSource.paginator) {
      this.dataSource.paginator.firstPage();
    }
  }

  addToCart(product: Product) {
    this.store.addToCart(product)
    const config = new MatSnackBarConfig();
    config.duration = 1300;
    this.snackBar.open('Added to cart', 'Close', config);
  }

  search() {
    const filterValue = this.searchForm.get('searchInput')?.value || '';
    this.applyFilter(filterValue);
  }

  details(id: number) {
    this.router.navigate(['/products', id]);
  }
}
