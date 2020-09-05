import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';


import { User } from '@app/_models';
import { AccountService } from '@app/_services';

@Component({ templateUrl: 'workspace.component.html' })
export class WorkspaceComponent {
    user: User;

    constructor(private accountService: AccountService) {
        this.user = this.accountService.userValue;
    }

    
}