import { Component } from '@angular/core';
import { TranslatorService } from './_services';

import { AccountService } from './_services';
import { User, Role } from './_models';

@Component({ selector: 'app', templateUrl: 'app.component.html' })
export class AppComponent {
    user: User;
    role = false;

    constructor(
        private accountService: AccountService,
        public translate: TranslatorService
        ) {
        if(this.accountService.userValue != null){
            this.user = this.accountService.userValue;
            this.role = (this.user.role === Role.Admin);
        }else{
            this.accountService.user.subscribe(x => this.user = x);
        }
    }

    switchLang(lang: string) {
        return this.translate.selectLanguage(lang);
    }

    get isAdmin() {
        return this.user && this.user.role === Role.Admin;
    }

    logout() {
        this.accountService.logout();
        location.reload();
    }

}

/** 
import { Component, OnInit } from '@angular/core';
import { TranslateService } from '@ngx-translate/core';

import { AccountService } from './_services';
import { User, Role } from './_models';

@Component({ selector: 'app', templateUrl: 'app.component.html' })
export class AppComponent {
    user: User;
    role = false;

    constructor(
        private accountService: AccountService,
        public translate: TranslateService
        ) {
        if(this.accountService.userValue != null){
            this.user = this.accountService.userValue;
            this.role = (this.user.role === Role.Admin);
        }else{
            this.accountService.user.subscribe(x => this.user = x);
        }
    }

    switchLang(lang: string) {
        return this.translate.use(lang);
    }

    get isAdmin() {
        return this.user && this.user.role === Role.Admin;
    }

    logout() {
        this.accountService.logout();
        location.reload();
    }

} */