import { Injectable } from '@angular/core';
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


    //probados ok
    addUser(id: string) {
      return this.http.get(`${environment.apiData}/newclient/${id}`);
    }

    deleteUser(id: string) {
      return this.http.delete(`${environment.apiData}/delete/${id}`);
    }
///
    getAll() {
        return this.http.get<File[]>(`${environment.apiData}/clientes`);
    }

    getAllFilesIndex(id: string) {
        console.log("llego aqui");
        return this.http.get<File[]>(`${environment.apiData}/filesindex/${id}`)
        .pipe(map(x => {
            //x.forEach(element => {
                //this.files.push(element);
                    console.log(x);
                    //console.log(x.filesFVS);
                //}); 
            return x
        }));
    }

    getAllFiles(id: string) {
        console.log("llego aqui");
        return this.http.get<File[]>(`${environment.apiData}/files/${id}`)
        .pipe(map(x => {
            //x.forEach(element => {
                //this.files.push(element);
                    console.log(x);
                    //console.log(x.filesFVS);
                //}); 
            return x
        }));
    }

}