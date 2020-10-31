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
    data: Array<any>;
    totalRecords: number;
    page: number = 1 ;

    constructor(
        private formBuilder: FormBuilder,
        private accountService: AccountService,
        private filterService: FilterService,
        private alertService: AlertService
        ) {
        this.user = this.accountService.userValue;
        this.lookingfiles = new LookingFiles(this.user);
        this.data = new Array<any>();
    }
  
    ngOnInit() {
        this.filterService.getAllFiles(this.user.email)
            .pipe(first())
            .subscribe(files => this.files = files);
        
        this.form = this.formBuilder.group({
            search: ['', Validators.required]
        });
    }

    select(positive, negative, type){
        this.lookingfiles.positive = positive;
        this.lookingfiles.negative = negative; 
        this.lookingfiles.typefile = type;
    }

    search(){
        this.lookingfiles.wanted = this.form.value['search'];
        this.filterService.search(this.lookingfiles).subscribe((data) => {
            for(let element of Object.keys(data)){
                this.data[element]= {id:element, docid: data[element]['docid'], titulo: data[element]['titulo'], abstract: data[element]['abstract'], key_words: data[element]['key_words']}
            };
            this.totalRecords =  Object.keys(data).length;
        });
    }

    onChangePage(event){
        this.page = event;
    }
  }