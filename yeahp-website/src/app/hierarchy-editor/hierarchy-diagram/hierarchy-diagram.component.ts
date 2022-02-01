import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-hierarchy-diagram',
  templateUrl: './hierarchy-diagram.component.svg',
  styleUrls: ['./hierarchy-diagram.component.scss'],
})
export class HierarchyDiagramComponent implements OnInit {
  public nodeTransform: string;
  public nodeWidth: string;
  public nodeHeight: string;
  public nodeTextX: number;
  public nodeTextY: number;

  constructor() {
    this.nodeTransform = 'translate(50,400)';
    this.nodeWidth = '150px';
    this.nodeHeight = '40px';
    this.nodeTextX = 10;
    this.nodeTextY = 30;
  }

  ngOnInit(): void {}
}
