import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { GalleraService } from '../../services/gallera.service';

@Component({
  selector: 'app-catalogo-gallos',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './catalogo-gallos.component.html',
  styleUrl: './catalogo-gallos.component.css'
})
export class CatalogoGallosComponent implements OnInit {
  listaGallos: any[] = [];
  listaCategorias: any[] = [];
  listaProveedores: any[] = [];
  
  urlBackend: string = 'http://127.0.0.1:8000';
  cargando: boolean = false; 
  vistaActual: 'cliente' | 'admin' = 'cliente';
  carrito: any[] = [];
  nombreCliente: string = '';
  ciudadEnvio: string = '';
  mostrarModal: boolean = false;
  editando: boolean = false;
  fotoSeleccionada: File | null = null;

  galloForm: any = {
    id: null, name: '', description: '', unit_price: 0, units_in_stock: 0, age_months: 0, category_id: null, supplier_id: null
  };

  constructor(private galleraService: GalleraService) {}

  ngOnInit(): void {
    this.cargarDatosMaestros();
  }

  cargarDatosMaestros() {
    this.galleraService.getCategories().subscribe(cats => this.listaCategorias = cats || []);
    this.galleraService.getSuppliers().subscribe(provs => this.listaProveedores = provs || []);
    this.cargarInventario();
  }

  cargarInventario(): void {
    this.galleraService.getProducts().subscribe({
      next: (data) => this.listaGallos = data || [],
      error: (err: any) => console.error('Error al cargar inventario:', err)
    });
  }

  // --- MÉTODOS PARA MOSTRAR NOMBRES ---
  obtenerNombreCategoria(id: number): string {
    const cat = this.listaCategorias.find(c => c.id == id);
    return cat ? (cat.category_name || cat.name || cat.CategoryName || 'Línea ' + id) : 'N/A';
  }

  obtenerNombreProveedor(id: number): string {
    const prov = this.listaProveedores.find(p => p.id == id);
    return prov ? (prov.company_name || prov.name || prov.CompanyName || 'Criadero ' + id) : 'N/A';
  }

  // --- GUARDADO CON MANEJO DE ERRORES ---
  guardarGallo(): void {
    if (!this.galloForm.name || !this.galloForm.category_id || !this.galloForm.supplier_id) {
      alert('Completa los campos obligatorios.');
      return;
    }
    this.cargando = true;
    const operacion = this.editando 
      ? this.galleraService.updateProduct(this.galloForm.id, this.galloForm)
      : this.galleraService.createProduct(this.galloForm);

    operacion.subscribe({
      next: (res: any) => {
        if (this.fotoSeleccionada) this.subirFoto(this.editando ? this.galloForm.id : res.id);
        else { alert('¡Guardado!'); this.cerrarModal(); this.cargarInventario(); }
      },
      error: (err: any) => { alert('Error al guardar.'); this.cargando = false; }
    });
  }

  subirFoto(productId: number): void {
    this.galleraService.uploadProductImage(productId, this.fotoSeleccionada!).subscribe({
      next: () => { this.cerrarModal(); this.cargarInventario(); },
      error: (err: any) => { console.error(err); this.cargando = false; }
    });
  }

  // --- MÉTODOS SIMULADOS PARA EVITAR ERRORES DE COMPILACIÓN ---
  crearNuevaLinea(): void {
    const nombre = prompt('Ingresa nombre de la nueva Línea:');
    if (nombre) this.listaCategorias.push({ id: Date.now(), category_name: nombre });
  }

  crearNuevoCriadero(): void {
    const nombre = prompt('Ingresa nombre del nuevo Criadero:');
    if (nombre) this.listaProveedores.push({ id: Date.now(), company_name: nombre });
  }

  abrirModalNuevo(): void { this.editando = false; this.galloForm = { id: null, name: '', category_id: null, supplier_id: null }; this.mostrarModal = true; }
  abrirModalEditar(gallo: any): void { this.editando = true; this.galloForm = { ...gallo }; this.mostrarModal = true; }
  cerrarModal(): void { this.mostrarModal = false; this.cargando = false; }
  onFotoSeleccionada(event: any): void { this.fotoSeleccionada = event.target.files[0]; }
  
  // ... resto de métodos (carrito, eliminar, etc) ...
  agregarAlCarrito(gallo: any): void { /* tu lógica */ }
  removerDelCarrito(index: number): void { this.carrito.splice(index, 1); }
  get totalCarrito(): number { return this.carrito.reduce((sum, item) => sum + (item.unit_price * item.quantity), 0); }
  finalizarCompra(): void { /* tu lógica */ }
  eliminarGallo(id: number): void { this.galleraService.deleteProduct(id).subscribe(() => this.cargarInventario()); }
}