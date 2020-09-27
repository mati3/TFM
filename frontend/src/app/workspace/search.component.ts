import { Component } from '@angular/core';
import { first } from 'rxjs/operators';

import { User, LookingFiles } from '@app/_models';
import { AccountService, AlertService, FilterService } from '@app/_services';

@Component({ templateUrl: 'search.component.html' })
export class SearchComponent {

    user: User;
    lookingfiles = null;
    files = null;
  
    constructor(
        private accountService: AccountService,
        private filterService: FilterService,
        private alertService: AlertService
        ) {
        this.user = this.accountService.userValue;
        this.lookingfiles = new LookingFiles(this.user);
    }
  
    ngOnInit() {
        this.filterService.getAllFiles(this.user.email)
            .pipe(first())
            .subscribe(files => this.files = files);
    }

    select(positive, negative, type){
        this.lookingfiles.positive = positive;
        this.lookingfiles.negative = negative; 
        this.lookingfiles.typefile = type;
    }

    search(word){
        this.lookingfiles.wanted = word;
        console.log(this.lookingfiles);
        this.filterService.search(this.lookingfiles);
    }
  }