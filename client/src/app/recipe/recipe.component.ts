import { Component } from '@angular/core';
import { SocketService } from '../web-socket.service';
import { FormGroup, FormControl } from '@angular/forms';

@Component({
  selector: 'app-recipe',
  templateUrl: './recipe.component.html',
  styleUrls: ['./recipe.component.scss'],
  host: {class:"flex flex-col flex-1 p-4 h-full"}
})
export class RecipeComponent {
  public message = "## **FreshBot**: Let's cook something!";
  public userForm = new FormGroup({
    userInput: new FormControl('')
  });

  constructor(public socket: SocketService) {}

  ngOnInit(): void {
    this.socket.getMessage('simple-recipe').subscribe((data: any) => {
      this.message += data.text;
    })
  }

  sendMessage(event?: Event) {
    const newInput = this.userForm.value.userInput;
    this.message += `\n## **User**: ${newInput}`
    this.message += '\n## **FreshBot**: ';
    this.socket.sendMessage('simple-recipe', this.userForm.value.userInput as string);
    this.userForm.reset();
  }
}
