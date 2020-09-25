﻿import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { environment } from '@environments/environment';

@Injectable({ providedIn: 'root' })
export class FilterService {

    constructor(
        private http: HttpClient,
    ) {
    }

    upload(email: string,typefile: String,formData: FormData){
        return this.http.post(`${environment.apiData}/upload/${email}/${typefile}`, formData)
            .subscribe();
    }

    deleteIndex(email: string,typefile: String){
        return this.http.delete(`${environment.apiData}/removefile/${email}/${typefile}`)
            .subscribe();
    }

    addUser(id: string) {
      return this.http.get(`${environment.apiData}/newclient/${id}`);
    }

    deleteUser(id: string) {
      return this.http.delete(`${environment.apiData}/delete/${id}`);
    }

    getAll() {
        return this.http.get<File[]>(`${environment.apiData}/clientes`);
    }

    getAllFilesIndex(id: string) {
        return this.http.get<File[]>(`${environment.apiData}/filesindex/${id}`)
        .pipe(map(x => { return x }));
    }

    getAllFiles(id: string) {
        return this.http.get<File[]>(`${environment.apiData}/files/${id}`)
        .pipe(map(x => { return x }));
    }

}