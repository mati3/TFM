import { Component } from '@angular/core';
import { first } from 'rxjs/operators';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { User, LookingFiles } from '@app/models';
import { AccountService, AlertService, FilterService } from '@app/services';

@Component({ templateUrl: 'search.component.html' })
export class SearchComponent {

    form: FormGroup;
    user: User;
    lookingfiles = null;
    files = null;
    result = null;
  
    constructor(
        private formBuilder: FormBuilder,
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
        
        this.form = this.formBuilder.group({
            search: ['', Validators.required]
        });
        console.log(this.form.value)
    }

    select(positive, negative, type){
        this.lookingfiles.positive = positive;
        this.lookingfiles.negative = negative; 
        this.lookingfiles.typefile = type;
    }

    search(){
        console.log(this.form.value['search'])
        this.lookingfiles.wanted = this.form.value['search'];
        console.log(this.lookingfiles);
        this.filterService.search(this.lookingfiles)
            .pipe(first())
            .subscribe(x => this.result = x);
    }
  }