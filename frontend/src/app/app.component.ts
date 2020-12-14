import { Component } from '@angular/core';
import { TranslatorService } from './services';

import { AccountService } from './services';
import { User, Role } from './models';

@Component({ selector: 'app', templateUrl: 'app.component.html' })
export class AppComponent {
    /**
     * @ignore
     */
    user: User;

    /**
     * @ignore
     */
    constructor(
        private accountService: AccountService,
        public translate: TranslatorService
        ) {
        //if(this.accountService.userValue != null){
          //  this.user = this.accountService.userValue;
        //}else{
            this.accountService.user.subscribe(x => this.user = x);
        //}
    }

    /**
     * @param {string} lang - language selected
     */
    switchLang(lang: string) {
        return this.translate.selectLanguage(lang);
    }

    /**
     * Checks if the current user is an admin
     * 
     * @return {boolean} 
     */
    get isAdmin() {
        if (this.user){
            return this.user && this.user[0].role === Role.Admin;
        }
        return this.user && this.user.role === Role.Admin;
    }
    /**
     * Logout for the current user
     */
    logout() {
        this.accountService.logout();
        //location.reload();
    }
}
