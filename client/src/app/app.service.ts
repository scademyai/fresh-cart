import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { StoreService } from './store.service';

@Injectable({
  providedIn: 'root'
})
export class AppService {

  constructor(private store: StoreService, private router: Router) { }

  init() {
    this.store.refresh();
    this.store.getCart();
  }

}
