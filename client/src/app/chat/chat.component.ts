import { Component } from '@angular/core';
import { SocketResponse, SocketService } from '../web-socket.service';
import { FormGroup, FormControl } from '@angular/forms';
import { Product } from '../store/types';
import { StoreService } from '../store.service';
import { MatSnackBar, MatSnackBarConfig } from '@angular/material/snack-bar';

@Component({
  selector: 'chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.scss'],
  host: {class:"flex flex-col flex-1 p-4 h-full"}
})
export class ChatComponent {
  public message = '## **FreshBot**: Hi, how can I help you?';
  public products: Product[] = [];
  public userForm = new FormGroup({
    userInput: new FormControl('')
  });

  constructor(public socket: SocketService, private store: StoreService, private snackBar: MatSnackBar) {}

  ngOnInit(): void {
    // TODO: Change this message type according to the current exercise
    this.socket.getMessage('freshbot').subscribe((data: SocketResponse) => {
      if (data.text)
        this.message += data.text;
      if (data.json)
        this.products.push(this.parseJson(data.json));
      if (data.cart)
        this.store.setCart({cart: data.cart});
    });
  }

  sendMessage(event?: Event) {
    const newInput = this.userForm.value.userInput;
    this.message += `\n## **User**: ${newInput}`
    this.message += '\n## **FreshBot**: ';
    // TODO: Change this message type according to the current exercise
    this.socket.sendMessage('freshbot', this.userForm.value.userInput as string);
    this.userForm.reset();
  }

  reloadChat() {
    this.userForm.reset();
    this.message = '## **FreshBot**: Hi, how can I help you?';
    this.products = [];
  }

  addToCart(product: Product) {
    this.store.addToCart(product)
    const config = new MatSnackBarConfig();
    config.duration = 1300;
    this.snackBar.open('Added to cart', 'Close', config);
  }

  private parseJson(json: string) {
    let parsedJson = JSON.parse(json);
    let product: Product = {
      name: parsedJson.name,
      quantity: parsedJson.quantity,
      id: parsedJson.id || -1,
      price: parsedJson.price || -1,
    };
    return product;
  }
}
