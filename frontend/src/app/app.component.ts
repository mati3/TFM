import { Component } from '@angular/core';
import { TranslatorService } from './_services';

import { AccountService } from './_services';
import { User, Role } from './_models';

@Component({ selector: 'app', templateUrl: 'app.component.html' })
export class AppComponent {
    user: User;

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

    switchLang(lang: string) {
        return this.translate.selectLanguage(lang);
    }

    get isAdmin() {
        if (this.user){
            return this.user && this.user[0].role === Role.Admin;
        }
        return this.user && this.user.role === Role.Admin;
    }

    logout() {
        this.accountService.logout();
        //location.reload();
    }
}
