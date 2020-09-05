import { Role } from "./role";

export class User {
    id: string;
    username: string;
    password: string;
    email: string;
    first_name: string;
    last_name: string;
    token?: string;
    role: Role;

}