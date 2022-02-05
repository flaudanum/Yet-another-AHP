import { Component, OnInit } from '@angular/core';
import { HierarchyNodePresentation } from './hierarchy-node-presentation';

@Component({
  selector: 'app-hierarchy-diagram',
  templateUrl: './hierarchy-diagram.component.svg',
  styleUrls: ['./hierarchy-diagram.component.scss'],
})
export class HierarchyDiagramComponent implements OnInit {
  public hierarchyNodes: HierarchyNodePresentation[] = [];

  constructor() {
    const newNode = new HierarchyNodePresentation('The Goal');
    newNode.transform = 'translate(50,300)';
    this.hierarchyNodes.push(newNode);
  }

  ngOnInit(): void {
    console.log(document.getElementsByTagName('text'));
  }
}
