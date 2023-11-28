import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { map } from 'rxjs/operators';
import { Observable } from 'rxjs';

import { take } from 'rxjs/operators';
import { Router } from '@angular/router';
import { AppService } from './app.service';
import { StoreService } from './store.service';
import { CartState } from './store/types';
import { HttpService } from './http.service';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'client';
  cartSize$: Observable<number | undefined>;
  loggedIn: Boolean = !!localStorage.getItem('token');
  name: string = 'John Doe';

  constructor(private http: HttpService, private router: Router, private appService: AppService, private store: StoreService) {
    this.router.events.subscribe(() => {
      this.appService.init()
    });
    this.cartSize$ = this.store.cart$.pipe(map((cart: CartState) => cart.data.cart.reduce((acc, item) => acc + item.quantity, 0)));
   }

  login() {
    this.http.get('/api/refresh-session').pipe(take(1)).subscribe((response: any) => {
      this.loggedIn = true;
      localStorage.setItem('token', response.access_token);
      window.location.reload();
    });
  }
  logout() {
    this.loggedIn = false;
    localStorage.clear();
    window.location.reload();
  }
}
