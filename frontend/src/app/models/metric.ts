export class Metric {
    tittle: string;
    description: string;
    value: number;
    
    constructor(t: string, d: string, v: number) {
        this.tittle = t;
        this.description = d;
        this.value = v;
    }
}