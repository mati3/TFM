import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { FileUploader } from 'ng2-file-upload';

import { environment } from '@environments/environment';

@Injectable({ providedIn: 'root' })
export class FilterService {

    constructor(
        private http: HttpClient,
    ) {
    }

    fileUploader(file: File){
        console.log(file)
        return new FileUploader({
            url: `${environment.apiData}/upload`,
            disableMultipart: true, // 'DisableMultipart' must be 'true' for formatDataFunction to be called.
            formatDataFunctionIsAsync: true,
            formatDataFunction: async (item) => {
              return new Promise( (resolve, reject) => {
                resolve({
                  name: item._file.name,
                  length: item._file.size,
                  contentType: item._file.type,
                  date: new Date(),
                  file: item.file.rawFile
                });
                console.log(item.file);
                console.log(item);
              });
            }
          });
    }

    add(file: File) {
        return this.http.post(`${environment.apiData}/file/add`, file);
    }

    getAll() {
        return this.http.get<File[]>(`${environment.apiData}/clientes`);
    }

    getAllFiles(id: string) {
        return this.http.get<File[]>(`${environment.apiData}/files/${id}`);
    }

    delete(id: string) {
        return this.http.delete(`${environment.apiData}/file/delete/${id}`);
    }

}