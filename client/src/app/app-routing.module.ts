import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CartComponent } from './cart/cart.component';
import { ChatComponent } from './chat/chat.component';
import { HomeComponent } from './home/home.component';
import { RecipeComponent } from './recipe/recipe.component';
import { ShopComponent } from './shop/shop.component';

const routes: Routes = [
  { path: 'shop', component: ShopComponent },
  { path: 'recipe', component: RecipeComponent },
  { path: 'cart', component: CartComponent },
  { path: '', component: HomeComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
