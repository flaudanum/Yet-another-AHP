import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HierarchyEditorLayoutComponent } from './hierarchy-editor-layout/hierarchy-editor-layout.component';
import { HierarchyDiagramComponent } from './hierarchy-diagram/hierarchy-diagram.component';
import { HierarchyEditorSidebarComponent } from './hierarchy-editor-sidebar/hierarchy-editor-sidebar.component';



@NgModule({
  declarations: [
    HierarchyEditorLayoutComponent,
    HierarchyDiagramComponent,
    HierarchyEditorSidebarComponent
  ],
  imports: [
    CommonModule
  ],
  exports: [
    HierarchyEditorLayoutComponent,
  ]
})
export class HierarchyEditorModule { }
