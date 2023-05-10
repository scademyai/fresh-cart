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
@UntilDestroy()
@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
  host: {class: 'p-4 w-full h-full'}
})
export class HomeComponent implements OnInit {
  
  ngOnInit() {
  }
}

