import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateFamiliarComponent } from './create-familiar.component';

describe('CreateFamiliarComponent', () => {
  let component: CreateFamiliarComponent;
  let fixture: ComponentFixture<CreateFamiliarComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [CreateFamiliarComponent]
    });
    fixture = TestBed.createComponent(CreateFamiliarComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
