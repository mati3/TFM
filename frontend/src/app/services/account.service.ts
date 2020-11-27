import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { environment } from '@environments/environment';
import { User } from '@app/models';

@Injectable({ providedIn: 'root' })
export class AccountService {
    /**
     * @ignore
     */
    private userSubject: BehaviorSubject<User>;

    public user: Observable<User>;

    /**
     * @ignore
     */
    constructor(
        private router: Router,
        private http: HttpClient
    ) {
        this.userSubject = new BehaviorSubject<User>(JSON.parse(localStorage.getItem('user')));
        this.user = this.userSubject.asObservable();
    }

    /**
     * The current user
     * 
     * @return {String} - Current user
     */
    public get userValue(): User {
        // userSubject.value return to array, atributes to be in array[0]
        if(this.userSubject.value != null)return this.userSubject.value[0];
        return this.userSubject.value;
    }

    /**
     * Authenticate an user
     * 
     * @param {String} email 
     * @param {String} password
     * 
     * @return {String}
     */
    login(email, password) {
        return this.http.post<User>(`${environment.apiUrl}/api/users/authenticate`, { email, password })
            .pipe(map(user => {
                if (user[0].accept){
                    localStorage.setItem('user', JSON.stringify(user));
                    this.userSubject.next(user);
                    return user;
                }else {
                    return  user=null;        
                }
                     
            }));
    }

    /**
     * Logout current user
     */
    logout() {
        localStorage.removeItem('user');
        this.userSubject.next(null);
        this.router.navigate(['/account/login']);
    }

    /**
     * Register an User
     */
    register(user: User) {
        return this.http.post(`${environment.apiUrl}/api/user/register`, user);
    }

    /**
     * Accept an user
     * 
     * @param {String} id - User identification to be accept
     */
    accept(id: string) {
        return this.http.get(`${environment.apiUrl}/api/acceptuser/${id}`);
    }

    /**
     * Get a list of all users
     */
    getAll() {
        return this.http.get<User[]>(`${environment.apiUrl}/api/users`);
    }

    /**
     * Get an user by ID
     * 
     * @param {String} id - User identification
     */
    getById(id: string) {
        return this.http.get<User>(`${environment.apiUrl}/api/user/${id}`);
    }

    /**
     * Update an users
     * 
     * @param {String} id - User identification
     * @param {String} params - New parameters for the user
     */
    update(id, params) {
        return this.http.put(`${environment.apiUrl}/api/user/${id}`, params)
            .pipe(map(x => {
                if (id == this.userValue.id) {
                    const user = { ...this.userValue, ...params };
                    localStorage.setItem('user', JSON.stringify(user));
                    this.userSubject.next(user);
                }
                return x;
            }));
    }

    /**
     * Delete an user
     * 
     * @param {String} id - User identification
     */
    delete(id: string) {
        return this.http.delete(`${environment.apiUrl}/api/user/${id}`)
            .pipe(map(x => {
                if (id == this.userValue.id) {
                    this.logout();
                }
                return x;
            }));
    }
}