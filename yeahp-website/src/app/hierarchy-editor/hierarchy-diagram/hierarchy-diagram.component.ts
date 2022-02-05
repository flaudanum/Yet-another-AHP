import { Component, OnInit } from '@angular/core';
import { Graph } from 'src/app/models/graph.model';
import { Criterion, Hierarchy } from 'src/app/models/hierarchy.model';
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
    this.hierarchy = this._hierarchyService.get_hierarchy();
    this.refreshNodes();
  }

  refreshNodes(): void {
    this.hierarchyPresentation = [];
    // Asserts that hierarchy data is available
    if (this.hierarchy === undefined) {
      return;
    }
    // Presentation of the goal element
    const goalPres = new HierarchyNodePresentation(this.hierarchy.goal);

    // Pushes the goal presentation to the list of displayed presentations
    this.hierarchyPresentation.push(goalPres);

    // Creates a new node associated to the goal in the hierarchy graph
    this.graph.addNode(goalPres.id, goalPres);

    // let elements: Criterion[] = this.hierarchy.criteria;
    let queue: Array<[string, Criterion[]]> = [];
    queue.push([goalPres.id, this.hierarchy.criteria]);
    while (queue) {
      const item: [string, Criterion[]] | undefined = queue.shift();
      // Asserts type of criterion as undefined
      if (!item) {
        break;
      }
      queue = [...queue, ...this.growGraph(...item)];
    }
  }

  growGraph(
    parentId: string,
    children: Criterion[]
  ): Array<[string, Criterion[]]> {
    // Asserts that hierarchy data is available
    if (this.hierarchy === undefined) {
      return [];
    }
    const toBeQueued: Array<[string, Criterion[]]> = [];

    children.forEach((child: Criterion) => {
      // Presentation of the child element
      const elementPres = new HierarchyNodePresentation(child.title);

      // Pushes the child element's presentation to the list of displayed presentations
      this.hierarchyPresentation.push(elementPres);

      // Creates a new node associated to the child element in the hierarchy
      this.graph.addNode(elementPres.id, elementPres);

      // Creates an edge from the parent to the child element
      this.graph.addEdge(parentId, elementPres.id);

      // Grows the queue of elements to be processed
      toBeQueued.push([elementPres.id, child.subCriteria]);
    });

    return toBeQueued;
  }
}
