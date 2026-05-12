export type CardTables = "1" | "2"; // TODO

export interface TableWithCategory {
  category: string,
  name: string
}

export interface Dino {
  name: string;
  health: ([number, number, number] | null)[];
  text: string;
  is_enemy: boolean;
}

export interface Enemy extends Dino {
  difficulty: number;
  damage_dist: number;
  sift_dist: number;
}


interface ColorizeCode {
    style_bright: boolean
    style_normal: boolean;
    style_dim: boolean;

    fore_black: boolean;
    fore_red: boolean;
    fore_green: boolean;
    fore_blue: boolean;
    fore_cyan: boolean;
    fore_magenta: boolean;
    fore_yellow: boolean;

    back_red: boolean;
    back_green: boolean;
    back_blue: boolean;
    back_white: boolean;
    back_cyan: boolean;
}

export interface Card {
  bodyTextAsJSONCodes: [string, ColorizeCode | null][],
  id: number,
  name: string, // HTML
  plainName: string,
  plainText: string,
  table: CardTables[],
  text: string // HTML
}
