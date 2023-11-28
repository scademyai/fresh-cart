import { HttpClient } from '@angular/common/http';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { Observable } from 'rxjs';
import { TestScheduler } from 'rxjs/testing';

import { defaultProductState, StoreService } from './store.service';
import { LoadingState, Product, ProductState } from './store/types';
import { HttpService } from './http.service';

describe('StoreService', () => {
  let service: StoreService;
  let testScheduler: TestScheduler;
  let httpService: HttpService;
  const products: Product[] = [{id: 1, name: 'apple', quantity: 2, price:3.2}]
  const expectedState: ProductState = {
    state: LoadingState.Loaded,
    data: products
  }
  const fakeHttpResponse = products
  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [ HttpClientTestingModule ]
    });

    testScheduler = new TestScheduler((actual, expected) => {
      expect(actual).toEqual(expected);
    });
    httpService = TestBed.inject(HttpService);
    service = TestBed.inject(StoreService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  
  it('should return loading state', () => {
    service.state$.subscribe((state: ProductState) =>
      expect(state.state).toBe(LoadingState.Loading)
    );
  });

  it('should provide the latest data to observers', () => {
    testScheduler.run((helpers) => {
      const { expectObservable, cold } = helpers;
      const obs1Sub = '          ^---';
      const obs1Expected = cold('a-b-', {
        a: defaultProductState,
        b: expectedState,
      });
      const obs2Sub = '          ---^';
      const obs2Expected = cold('   b', { b: expectedState });
      const httpResponse = cold('--c-', { c: fakeHttpResponse });

      stubHttpService(httpResponse);
      service.refresh();

      expectObservable(service.state$, obs1Sub).toEqual(obs1Expected);
      expectObservable(service.state$, obs2Sub).toEqual(obs2Expected);
    });
  });

  it('should not emit new values on error', () => {
    testScheduler.run((helpers) => {
      const { expectObservable, cold } = helpers;
      const obs1Sub = '          ^--';
      const obs1Expected = cold('a--', {
        a: defaultProductState,
      });
      const httpResponse = cold('--#');

      stubHttpService(httpResponse);
      service.refresh();

      expectObservable(service.state$, obs1Sub).toEqual(obs1Expected);
    });
  });

 

  function stubHttpService(response: Observable<any>) {
    spyOn(httpService, 'get')
      .withArgs('/api/products')
      .and.returnValue(response);
  }

  function stubPostCart(product: Product, response: Observable<any>) {
    spyOn(httpService, 'post')
      .withArgs('/api/cart', {"cart": [product]})
      .and.returnValue(response);
  }
});
