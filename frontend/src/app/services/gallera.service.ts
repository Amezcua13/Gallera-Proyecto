import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class GalleraService {
  // La ruta de tu API en Python
  private apiUrl = 'http://127.0.0.1:8000';

  constructor(private http: HttpClient) { }

  // --- MÉTODOS PARA PRODUCTOS (GALLOS) ---
  
  // Obtener todos los gallos de los corrales
  getProducts(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/products`);
  }

  // Crear un nuevo gallo
  createProduct(product: any): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/products`, product);
  }

  // Editar los datos de un gallo existente
  updateProduct(productId: number, product: any): Observable<any> {
    return this.http.put<any>(`${this.apiUrl}/products/${productId}`, product);
  }

  // Eliminar un gallo del sistema
  deleteProduct(productId: number): Observable<any> {
    return this.http.delete<any>(`${this.apiUrl}/products/${productId}`);
  }

  // Subir la foto real del ejemplar amarrada a su ID
  uploadProductImage(productId: number, imageFile: File): Observable<any> {
    const formData = new FormData();
    formData.append('file', imageFile);
    return this.http.post<any>(`${this.apiUrl}/products/${productId}/upload-image`, formData);
  }

  // --- MÉTODOS PARA CATEGORÍAS (LÍNEAS DE SANGRE) ---
  
  // Obtener todas las líneas de aves (Hatch, Kelso, Albany...)
  getCategories(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/categories`);
  }

  // Crear una nueva línea de sangre
  createCategory(category: any): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/categories`, category);
  }
// --- MÉTODOS PARA ÓRDENES (VENTAS TRANSACCIONALES) ---
  
  // Enviar el pedido completo con los productos seleccionados a MySQL
  createOrder(order: any): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/orders`, order);
  }

  getSuppliers(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/suppliers`);
  }

}