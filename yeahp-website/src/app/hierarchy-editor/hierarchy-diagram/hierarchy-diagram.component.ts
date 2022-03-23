import { Component, OnInit } from '@angular/core';
import { Graph } from 'src/app/models/graph.model';
import { Hierarchy } from 'src/app/models/hierarchy.model';
import { HierarchyLayout } from 'src/app/models/hierarchy_layout.model';
import { HierarchyService } from 'src/app/services/hierarchy.service';
import { HierarchyNodePresentation } from './hierarchy-node-presentation';

@Component({
  selector: 'app-hierarchy-diagram',
  templateUrl: './hierarchy-diagram.component.svg',
  styleUrls: ['./hierarchy-diagram.component.scss'],
})
export class HierarchyDiagramComponent implements OnInit {
  public hierarchyPresentation: HierarchyNodePresentation[] = [];
  public hierarchy?: Hierarchy;
  private graph = new Graph<HierarchyNodePresentation>();

  constructor(private _hierarchyService: HierarchyService) {
    // const newNode = new HierarchyNodePresentation('The Goal');
    // newNode.transform = 'translate(50,300)';
    // this.hierarchyNodes.push(newNode);
  }

  ngOnInit(): void {
    this.hierarchy = this._hierarchyService.getHierarchy();
    this.refreshNodes();
  }

  refreshNodes(): void {
    this.hierarchyPresentation = [];
    // Asserts that hierarchy data is available
    if (this.hierarchy === undefined) {
      return;
    }

    this._hierarchyService
      .getHierarchyLayout(this.hierarchy)
      .subscribe((layout: HierarchyLayout) => {
        const yCoordMap: Map<string, number> = new Map();
        const depthMap: Map<string, number> = new Map();

        let depth: number = 0;
        layout.class_by_depth.forEach((depthClass: string[]) => {
          depthClass.forEach((node: string) => {
            depthMap.set(node, depth);
          });
          depth++;
        });

        layout.y_coordinates.forEach((coord: [string, number]) => {
          const node: string = coord[0];
          const yNormCoord: number = coord[1];
          yCoordMap.set(node, yNormCoord);
        });

        // Sets the offset so that the minimal normalized y-coordinate is 0
        HierarchyNodePresentation.yNormOffset = -Math.min(
          ...yCoordMap.values()
        );

        // Presentation of the goal element
        const goalPres = new HierarchyNodePresentation(
          this.hierarchy?.goal ?? 'Missing Goal'
        );

        goalPres.setLocation(0, 0);

        // Pushes the goal presentation to the list of displayed presentations
        this.hierarchyPresentation.push(goalPres);
        this.hierarchy?.criteria.forEach((criterion: string) => {
          // Presentation of the criterion element
          const criterionPres = new HierarchyNodePresentation(criterion);
          criterionPres.setLocation(
            depthMap.get(criterion) ?? 0,
            yCoordMap.get(criterion) ?? 0
          );

          // Pushes the criterion's presentation to the list of displayed presentations
          this.hierarchyPresentation.push(criterionPres);
        });
      });
  }
}
