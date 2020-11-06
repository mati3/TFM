import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { map } from 'rxjs/operators';

import { environment } from '@environments/environment';

@Injectable({ providedIn: 'root' })
export class FilterService {

    constructor(
        private http: HttpClient,
    ) {
    }

    /**
     * Enter and index the selected pair of files in the database
     * 
     * @param {FormData} formData - Pair of files (positive and negative), typefile and email
     * 
     * @return {String}
     */
    upload(formData: FormData){
        return this.http.post(`${environment.apiData}/upload`, formData)
            .subscribe();
    }

    /**
     * Search the content requested by the user in database
     * 
     * @param {Lookingfiles} id - Object containing the necessary data: file pair, search word, typefile, user identifier (email)
     * 
     * @return {List} - list of documents with docid, abstract, title and key_words attributes
     */
    search(id){
        return this.http.post(`${environment.apiData}/search`, id)
        .pipe(map(x => { return x }));
    }
    
    /**
     * When selecting a pair of TIS files, we request from the database all the terms of that pair of files, along with their frequency.
     * 
     * @param {Lookingfiles} id - Object containing the necessary data: file pair, search word, typefile, user identifier (email)
     * 
     * @return {Dic} - Dictionary with all {terms: frequency} of the positive and negative files of the selected pair of TIS files
     */
    selectTIS(id){
        return this.http.post(`${environment.apiData}/tis`, id)
        .pipe(map(x => { return x }));
    }

    /**
     * Applies the filter selected by the user, to the pair of TIS files previously selected
     * 
     * @param {Filter} id - Filter type object that contains: terms, frequency of positive and negative files, 
     * user identification (email), number of terms to return (sum) and selected filter
     * 
     * @return {List} - list of the best terms found with the filter
     */
    selectFilter(id){
        return this.http.post(`${environment.apiData}/filter`, id)
        .pipe(map(x => { return x }));
    }

    /**
     * Apply the selected filter on the file pair previously selected
     * 
     * @param {Lookingfiles} id - Object containing the necessary data: file pair, search word, typefile, user identifier (email)
     * 
     * @return {Dic} - Performance measures for each positive file
     */
    applyFilter(id){
        return this.http.post(`${environment.apiData}/applyFilter`, id)
        .pipe(map(x => { return x }));
    }

    /**
     * Delete all files in the selected file type group in the database
     * 
     * @param {String} email - User identifier
     * @param {String} typefile - File types to delete
     * 
     * @return {String} 
     */
    deleteIndex(email: string,typefile: String){
        return this.http.delete(`${environment.apiData}/removefile/${email}/${typefile}`)
            .subscribe();
    }

    /**
     * Add a new user to the Files database
     * 
     * @param {String} id - User identifier
     * 
     * @return {String} 
     */
    addUser(id: string) {
      return this.http.get(`${environment.apiData}/newclient/${id}`);
    }

    /**
     * Delete an user to the Files database
     * 
     * @param {String} id - User identifier 
     * 
     * @return {String} 
     */
    deleteUser(id: string) {
      return this.http.delete(`${environment.apiData}/delete/${id}`);
    }

    /**
     * Retrieves the names of the files associated with a user from the database
     * 
     * @param {String} id - User identifier
     * 
     * @return {Dict} - Dictionary with all user files in the database
     */
    getAllFiles(id: string) {
        return this.http.get<File[]>(`${environment.apiData}/files/${id}`)
        .pipe(map(x => { return x }));
    }

}