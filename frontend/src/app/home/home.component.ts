import { Component } from '@angular/core';

import { User } from '@app/_models';
import { AccountService } from '@app/_services';

@Component({ templateUrl: 'home.component.html' })
export class HomeComponent {
    user: User;

    constructor(private accountService: AccountService) {
        if(this.accountService.userValue != null){
            this.user = this.accountService.userValue;
        }else{
            this.accountService.user.subscribe(x => this.user = x);
        }
    }
    
}