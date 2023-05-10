import { HttpClient } from '@angular/common/http';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { Observable } from 'rxjs';
import { TestScheduler } from 'rxjs/testing';

import { defaultProductState, StoreService } from './store.service';
import { LoadingState, Product, ProductState } from './store/types';

describe('StoreService', () => {
  let service: StoreService;
  let testScheduler: TestScheduler;
  let httpClient: HttpClient;
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
    httpClient = TestBed.inject(HttpClient);
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

      stubHttpClient(httpResponse);
      service.refresh();

      expectObservable(service.state$, obs1Sub).toEqual(obs1Expected);
      // expectObservable(service.state$, obs2Sub).toEqual(obs2Expected);
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

      stubHttpClient(httpResponse);
      service.refresh();

      expectObservable(service.state$, obs1Sub).toEqual(obs1Expected);
    });
  });

  xit('addToCart should call the api', () => {
    testScheduler.run(({expectObservable, cold}) => {
      stubPostCart(products[0], cold('a--', {a: products}));

      const obsStub = '         ^--';
      const obsExpected = cold('a--', {a: products});

      expectObservable(service.addToCart(products[0]), obsStub).toEqual(obsExpected);
    });
  })  

  function stubHttpClient(response: Observable<any>) {
    spyOn(httpClient, 'get')
      .withArgs('/api/products')
      .and.returnValue(response);
  }

  function stubPostCart(product: Product, response: Observable<any>) {
    spyOn(httpClient, 'post')
      .withArgs('/api/cart', {"cart": [product]})
      .and.returnValue(response);
  }
});
