import { ComponentFixture, TestBed } from '@angular/core/testing';
import { SocketService } from '../web-socket.service';
import { config } from '../app.module'
import { RecipeComponent } from './recipe.component';
import { SocketIoModule } from 'ngx-socket-io';
import { MarkdownModule } from 'ngx-markdown';
import { MatFormFieldModule } from '@angular/material/form-field';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatInputModule } from '@angular/material/input';
import { ReactiveFormsModule } from '@angular/forms';
describe('RecipeComponent', () => {
  let component: RecipeComponent;
  let fixture: ComponentFixture<RecipeComponent>;
  let socketService: SocketService;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ RecipeComponent ],
      imports: [SocketIoModule.forRoot(config), MarkdownModule.forRoot(), MatFormFieldModule, BrowserAnimationsModule, ReactiveFormsModule, MatInputModule],
      providers: [ SocketService ]
    })
    .compileComponents();

    socketService = TestBed.inject(SocketService)
    fixture = TestBed.createComponent(RecipeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
