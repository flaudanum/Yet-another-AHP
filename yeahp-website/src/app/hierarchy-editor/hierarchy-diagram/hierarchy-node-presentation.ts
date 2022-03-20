const X_STEP = 300;
const Y_STEP = 100;
const BASE_WIDTH = 150;
const BASE_HEIGHT = 40;

export class HierarchyNodePresentation {
  private static idCounter: number = 0;
  private static _yOffset: number = 0;

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

  static set yNormOffset(value: number) {
    HierarchyNodePresentation._yOffset = value * Y_STEP + BASE_HEIGHT;
  }

  constructor(title: string) {
    this.title = title;

    // Standard dimensions of the box
    this._width = BASE_WIDTH; // px
    this._height = BASE_HEIGHT; // px

    this._textX = this._width * 0.5; // px
    this._textY = this._height * 0.5; // px
    this._id = `node-${HierarchyNodePresentation.idCounter}`;
    HierarchyNodePresentation.idCounter++;
  }

  setLocation(depth: number, normYCoord: number): void {
    this.transform = `translate(${depth * X_STEP}, ${
      normYCoord * Y_STEP + HierarchyNodePresentation._yOffset
    })`;
  }
}
