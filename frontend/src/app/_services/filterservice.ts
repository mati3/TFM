import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { environment } from '@environments/environment';
import { LookingFiles } from '@app/_models';

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

    search(id){
        console.log(" hasta aqui llego")
        return this.http.post(`${environment.apiData}/search`, id)
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

    // comprobar si se usa
    getAllFilesIndex(id: string) {
        return this.http.get<File[]>(`${environment.apiData}/filesindex/${id}`)
        .pipe(map(x => { return x }));
    }

    getAllFiles(id: string) {
        return this.http.get<File[]>(`${environment.apiData}/files/${id}`)
        .pipe(map(x => { return x }));
    }

}