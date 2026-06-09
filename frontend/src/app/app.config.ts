import { ApplicationConfig, provideZoneChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient } from '@angular/common/http'; // Herramienta de conexión

import { routes } from './app.routes';

export const appConfig: ApplicationConfig = { // <-- CAMBIADO A appConfig
  providers: [
    provideZoneChangeDetection({ eventCoalescing: true }), 
    provideRouter(routes),
    provideHttpClient() // Activamos comunicación con tu API
  ]
};