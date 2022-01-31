import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HierarchyEditorLayoutComponent } from './hierarchy-editor-layout.component';

describe('HierarchyEditorLayoutComponent', () => {
  let component: HierarchyEditorLayoutComponent;
  let fixture: ComponentFixture<HierarchyEditorLayoutComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ HierarchyEditorLayoutComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(HierarchyEditorLayoutComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
