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
        this.lookingfiles = new LookingFiles(this.user.email);
        this.data = new Array<any>();
    }
  
    /**
     * Shows all user files in database
     */
    ngOnInit() {
        this.filterService.getAllFiles(this.user.email)
            .pipe(first())
            .subscribe(files => this.files = files);
        
        this.form = this.formBuilder.group({
            search: ['', Validators.required]
        });
    }

    /**
     * Select pair of files 
     * 
     * @param {String} positive - File positive
     * @param {String} negative - File negative
     * @param {String} type - Type of file
     */
    select(positive, negative, type){
        this.lookingfiles.positive = positive;
        this.lookingfiles.negative = negative; 
        this.lookingfiles.typefile = type;
    }

    /**
     * Search the content requested by the user
     */
    search(){
        this.lookingfiles.wanted = this.form.value['search'];
        this.filterService.search(this.lookingfiles).subscribe((data) => {
            for(let element of Object.keys(data)){
                this.data[element]= {id:element, docid: data[element]['docid'], titulo: data[element]['titulo'], abstract: data[element]['abstract'], key_words: data[element]['key_words']}
            };
            this.totalRecords =  Object.keys(data).length;
        });
    }

    /**
     * Pagination
     */
    onChangePage(event){
        this.page = event;
    }
  }