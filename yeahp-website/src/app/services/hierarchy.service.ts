import { Injectable } from '@angular/core';
import { Hierarchy } from '../models/hierarchy.model';
import { hierarchyChooseAirline } from './hierarchy.fake.data';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { HierarchyLayout } from '../models/hierarchy_layou.model';

@Injectable({
  providedIn: 'root',
})
export class HierarchyService {
  constructor(private _httpClient: HttpClient) {}

  getHierarchy(): Hierarchy {
    return hierarchyChooseAirline;
  }

  getHierarchyLayout(): Observable<HierarchyLayout> {
    return this._httpClient.post<HierarchyLayout>(
      'localhost:8000/hierarchy/layout/',
      {}
    );
  }
}
