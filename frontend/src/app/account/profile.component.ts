import { Component } from '@angular/core';
import { User } from '@app/models';
import { AccountService } from '@app/services';

@Component({ templateUrl: 'profile.component.html' })
export class ProfileComponent {

    /**
     * Current user
     */
    user: User;

    /**
     * @ignore
     */
    constructor(
        private accountService: AccountService
        ) {
        this.user = this.accountService.userValue;
    } 
    
}
