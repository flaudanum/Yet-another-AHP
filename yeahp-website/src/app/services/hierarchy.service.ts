import { Injectable } from '@angular/core';
import { Hierarchy } from '../models/hierarchy.model';
import { hierarchyChooseAirline } from './hierarchy.fake.data';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import {
  HierarchyLayout,
  HierarchyLayoutPayload,
} from '../models/hierarchy_layout.model';

@Injectable({
  providedIn: 'root',
})
export class HierarchyService {
  constructor(private _httpClient: HttpClient) {}

  getHierarchy(): Hierarchy {
    return hierarchyChooseAirline;
  }

  getHierarchyLayout(hierarchy: Hierarchy): Observable<HierarchyLayout> {
    const payload: HierarchyLayoutPayload = {
      root: hierarchy.goal,
      dependencies: hierarchy.dependencies,
    };
    // TODO: configure CORS on backend
    return this._httpClient.post<HierarchyLayout>(
      'http://localhost:8000/hierarchy/layout/',
      payload
    );
  }
}
