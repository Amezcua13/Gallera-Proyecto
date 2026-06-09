import { TestBed } from '@angular/core/testing';

import { GalleraService } from './gallera.service';

describe('GalleraService', () => {
  let service: GalleraService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(GalleraService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});