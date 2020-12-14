import { Component } from '@angular/core';

import { User } from '@app/models';
import { AccountService } from '@app/services';

@Component({ templateUrl: 'home.component.html' })
export class HomeComponent {
    /**
     * Current user
     */
    user: User;

    /**
     * @ignore
     */
    constructor(private accountService: AccountService) {
        if(this.accountService.userValue != null){
            this.user = this.accountService.userValue;
        }else{
            this.accountService.user.subscribe(x => this.user = x);
        }
    }
    
}