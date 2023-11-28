import { TestBed, fakeAsync, tick } from '@angular/core/testing';
import { Router } from '@angular/router';
import { RouterTestingModule } from '@angular/router/testing';
import { routes } from './app-routing.module';
import { Location } from '@angular/common';
import { HttpClientTestingModule } from '@angular/common/http/testing';

describe('AppRouting', () => {
  let location: Location;
  let router: Router;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        HttpClientTestingModule,
        RouterTestingModule.withRoutes(routes),
      ],
    }).compileComponents();
  });

  beforeEach(() => {
    router = TestBed.inject(Router);
    location = TestBed.inject(Location);
    router.initialNavigation();
  });

  const slugs = ['/shop', '/cart', '/'];

  slugs.forEach((slug: string) => {
    it(`${slug} should work`, fakeAsync(() => {
      router.navigate([slug]);
      tick();
      expect(location.path()).toEqual(slug);
    }));
  });
});
