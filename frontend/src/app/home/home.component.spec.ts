import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { HomeComponent } from './home.component';
import { MatPaginator, MatPaginatorModule } from '@angular/material/paginator';
import { SocketService } from '../web-socket.service';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { RunHelpers, TestScheduler } from 'rxjs/testing';
import { MatTableDataSource, MatTableModule } from '@angular/material/table';
import { defaultProductState, StoreService } from '../store.service';
import { MatSnackBarModule } from '@angular/material/snack-bar';

import { EMPTY, of } from 'rxjs';

import { ActivatedRoute } from '@angular/router';
import { Product } from '../store/types';

describe('HomeComponent', () => {
  let component: HomeComponent;
  let fixture: ComponentFixture<HomeComponent>;
  let testScheduler: TestScheduler;
  let httpTestingController: HttpTestingController
  const dataSourceSpy = jasmine.createSpyObj('MatTableDataSource', ['connect']);
  const paginatorSpy = jasmine.createSpyObj('MatPaginator', ['pageIndex', 'pageSize', 'length']);
  const store: any = { state$: EMPTY };
  const products: Product[] = [{id: 1, name: 'apple', quantity: 2, price:3.2}]

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ HomeComponent ],
      imports: [ HttpClientTestingModule, MatPaginatorModule, BrowserAnimationsModule, MatTableModule, MatSnackBarModule ],
      providers: [SocketService, StoreService, 
        { provide: MatTableDataSource, useValue: dataSourceSpy },
        { provide: MatPaginator, useValue: paginatorSpy },
      {
          provide: ActivatedRoute,
          useValue: {
            queryParamMap: of(new Map())
          }
        },
        {
          provide: StoreService,
          useValue: store,
        },]
    })
    .compileComponents();

    testScheduler = new TestScheduler((actual, expected) => {
      expect(actual).toEqual(expected);
    });
    fixture = TestBed.createComponent(HomeComponent);
    component = fixture.componentInstance;
    httpTestingController = TestBed.inject(HttpTestingController);
    fixture.detectChanges();
  });

  afterEach(() => {
    httpTestingController.verify();
  })

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
