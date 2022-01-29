import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HierarchyEditorLayoutComponent } from './hierarchy-editor/hierarchy-editor-layout/hierarchy-editor-layout.component';

const routes: Routes = [
  { path: 'edit-hierarchy', component: HierarchyEditorLayoutComponent },
  { path: '',   redirectTo: '/edit-hierarchy', pathMatch: 'full' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
