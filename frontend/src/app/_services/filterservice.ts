import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { environment } from '@environments/environment';
import { User } from '@app/_models';
import { AccountService } from '@app/_services';

@Injectable({ providedIn: 'root' })
export class FilterService {
    private userSubject: BehaviorSubject<User>;

    constructor(
        private router: Router,
        private http: HttpClient,
        private accountService: AccountService
    ) {
        this.userSubject = this.accountService.userValue;
    }

    add(file: File) {
        return this.http.post(`${environment.apiUrl}/api/file/add`, file);
    }

    getAll() {
        return this.http.get<File[]>(`${environment.apiUrl}/api/files`);
    }

    delete(id: string) {
        return this.http.delete(`${environment.apiUrl}/api/file/${id}`);
    }
}