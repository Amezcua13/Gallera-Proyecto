import { Component } from '@angular/core';
import { CatalogoGallosComponent } from './components/catalogo-gallos/catalogo-gallos.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CatalogoGallosComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'frontend-gallera';
}