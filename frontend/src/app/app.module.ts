import { APP_INITIALIZER, NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatListModule } from '@angular/material/list';
import { SocketIoModule, SocketIoConfig } from 'ngx-socket-io';
import { ReactiveFormsModule } from '@angular/forms';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MarkdownModule,  MarkedOptions } from 'ngx-markdown';
import { MatCardModule } from '@angular/material/card';
import { HttpClientModule } from '@angular/common/http';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatTableModule } from '@angular/material/table';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatGridListModule } from '@angular/material/grid-list';
import { MatBadgeModule } from '@angular/material/badge';
import {MatTooltipModule} from '@angular/material/tooltip';


import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { CartComponent } from './cart/cart.component';
import { SocketService } from './web-socket.service';
import { ChatComponent } from './chat/chat.component';
import { HomeComponent } from './home/home.component';
import { AppService } from './app.service';
import { ShopComponent } from './shop/shop.component';
import { ProductPageComponent } from './product-page/product-page.component';
import { PrivacyPolicyComponent } from './privacy-policy/privacy-policy.component';
import { TermsOfServiceComponent } from './terms-of-service/terms-of-service.component';
export const config: SocketIoConfig = { url: 'http://localhost:9090', options: {} };

export function initializeApp(appService: AppService) {
  return () => {
    appService.init();
  };
}

@NgModule({
  declarations: [
    AppComponent,
    CartComponent,
    ChatComponent,
    HomeComponent,
    ShopComponent,
    ProductPageComponent,
    PrivacyPolicyComponent,
    TermsOfServiceComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    MatButtonModule,
    MatIconModule,
    MatInputModule,
    MatListModule,
    ReactiveFormsModule,
    MatToolbarModule,
    MatCardModule,
    HttpClientModule,
    MatPaginatorModule,
    MatTableModule,
    MatSnackBarModule,
    MatGridListModule,
    MatBadgeModule,
    MatTooltipModule,
    BrowserAnimationsModule,
    SocketIoModule.forRoot(config),
    MarkdownModule.forRoot({markedOptions: {
      provide: MarkedOptions,
      useValue: {
        gfm: true,
        breaks: false,
        pedantic: true,
        smartLists: true,
        smartypants: false,
      }
    }})
  ],
  providers: [
    SocketService,
    AppService,
    {
      provide: APP_INITIALIZER,
      useFactory: initializeApp,
      deps: [AppService],
      multi: true,
    },
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
