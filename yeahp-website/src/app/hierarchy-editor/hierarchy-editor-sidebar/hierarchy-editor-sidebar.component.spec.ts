import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HierarchyEditorSidebarComponent } from './hierarchy-editor-sidebar.component';

describe('HierarchyEditorSidebarComponent', () => {
  let component: HierarchyEditorSidebarComponent;
  let fixture: ComponentFixture<HierarchyEditorSidebarComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ HierarchyEditorSidebarComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(HierarchyEditorSidebarComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
