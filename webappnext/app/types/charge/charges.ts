export interface ChargeState {
    Charge: number;
    CM: number;
    TD: number;
    TP: number;
}

export type ChargeType = keyof ChargeState