import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HierarchyEditorModule } from './hierarchy-editor/hierarchy-editor.module';

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HierarchyEditorModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
