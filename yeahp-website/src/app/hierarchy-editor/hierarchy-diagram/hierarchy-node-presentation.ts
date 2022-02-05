export class HierarchyNodePresentation {
  private static idCounter: number = 0;

  public transform: string = '';
  private _width: number = 0;
  private _height: number = 0;
  private _textX: number = 0;
  private _textY: number = 0;
  public title: string;
  private _id: string;

  get width(): number {
    return this._width;
  }

  get pxWidth(): string {
    return `${this.width}px`;
  }

  get height(): number {
    return this._height;
  }

  get pxHeight(): string {
    return `${this.height}px`;
  }

  get textX(): number {
    return this._textX;
  }

  get pxTextX(): string {
    return `${this.textX}px`;
  }

  get textY(): number {
    return this._textY;
  }

  get pxTextY(): string {
    return `${this.textY}px`;
  }

  get id(): string {
    return this._id;
  }

  constructor(title: string) {
    this.title = title;

    // Standard dimensions of the box
    this._width = 150; // px
    this._height = 40; // px

    this._textX = this._width * 0.5; // px
    this._textY = this._height * 0.5; // px
    this._id = `node-${HierarchyNodePresentation.idCounter}`;
    HierarchyNodePresentation.idCounter++;
  }
}
