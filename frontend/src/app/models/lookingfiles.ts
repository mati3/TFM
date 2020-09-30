import { User } from "./user";

export class LookingFiles {
    id: User;
    typefile: string;
    positive: File;
    negative: File;
    wanted: string;

    constructor(id: User) {
        this.id = id;
        this.typefile = "";
        this.positive = null;
        this.negative = null;
        this.wanted = "";
    }
}