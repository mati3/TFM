import { User } from "./user";

export class LookingFiles {
    email: string;
    typefile: string;
    positive: File;
    negative: File;
    wanted: string;

    constructor(id: string) {
        this.email = id;
        this.typefile = "";
        this.positive = null;
        this.negative = null;
        this.wanted = "";
    }
}