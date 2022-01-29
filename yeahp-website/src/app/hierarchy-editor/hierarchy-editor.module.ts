import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HierarchyEditorLayoutComponent } from './hierarchy-editor-layout/hierarchy-editor-layout.component';



@NgModule({
  declarations: [
    HierarchyEditorLayoutComponent
  ],
  imports: [
    CommonModule
  ],
  exports: [
    HierarchyEditorLayoutComponent
  ]
})
export class HierarchyEditorModule { }
