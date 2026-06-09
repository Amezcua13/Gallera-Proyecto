import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CatalogoGallosComponent } from './catalogo-gallos.component';

describe('CatalogoGallosComponent', () => {
  let component: CatalogoGallosComponent;
  let fixture: ComponentFixture<CatalogoGallosComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CatalogoGallosComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CatalogoGallosComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
