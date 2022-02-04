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
    newNode.transform = 'translate(50,400)';
    newNode.width = 150;
    newNode.height = 40;
    newNode.textX = 10;
    newNode.textY = 30;
    this.hierarchyNodes.push(newNode);
  }

  ngOnInit(): void {}
}
