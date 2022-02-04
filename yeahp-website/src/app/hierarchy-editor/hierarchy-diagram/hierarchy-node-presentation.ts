export class HierarchyNodePresentation {
  public transform: string = '';
  public width: number = 0;
  public height: number = 0;
  public textX: number = 0;
  public textY: number = 0;
  public title: string;

  get pxWidth(): string {
    return `${this.width}px`;
  }

  get pxHeight(): string {
    return `${this.height}px`;
  }

  get pxTextX(): string {
    return `${this.textX}px`;
  }

  get pxTextY(): string {
    return `${this.textY}px`;
  }

  constructor(title: string) {
    this.title = title;
  }
}
