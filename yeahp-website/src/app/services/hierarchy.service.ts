import { Injectable } from '@angular/core';
import { hierarchyChooseAirline } from './hierarchy.fake.data';

@Injectable({
  providedIn: 'root',
})
export class HierarchyService {
  constructor() {}

  get_hierarchy(): Hierarchy {
    return hierarchyChooseAirline;
  }
}
