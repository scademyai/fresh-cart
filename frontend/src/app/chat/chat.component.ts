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
  host: {class:"flex flex-col flex-1 p-4 h-full w-full break-words"}
})
export class ChatComponent {
  public message = '## **FreshBot**: Hi, how can I help you?';
  public products: Product[] = [];
  public userForm = new FormGroup({
    userInput: new FormControl('')
  });
  private SOCKET_MESSAGE_TYPE = 'freshbot';

  container: HTMLElement; 

  constructor(public socket: SocketService, private store: StoreService, private snackBar: MatSnackBar) {}


  scrollAutomatically() {
    this.container = document.getElementById("chatContainer")!;
    this.container.scrollTop = this.container.scrollHeight;   
  }
  ngOnInit(): void {
    this.socket.getMessage(this.SOCKET_MESSAGE_TYPE).subscribe((data: SocketResponse) => {
      if (data.text)
        this.message += data.text;
        this.scrollAutomatically();
      if (data.json)
        this.products.push(this.parseJson(data.json));
      if (data.cart)
        this.store.setCart({cart: data.cart});
    });
  }

  sendMessage(event?: Event) {
    event?.preventDefault();
    const newInput = this.userForm.value.userInput;
    this.message += `\n## **User**: ${newInput}`
    this.message += '\n## **FreshBot**: ';
    this.socket.sendMessage(this.SOCKET_MESSAGE_TYPE, this.userForm.value.userInput as string);
    this.userForm.reset();
    this.products = [];
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

  private parseJson(parsedJson: Product): Product {
    return {
      name: parsedJson.name,
      quantity: parsedJson.quantity,
      id: parsedJson.id || -1,
      price: parsedJson.price || -1,
    };
  }
}
