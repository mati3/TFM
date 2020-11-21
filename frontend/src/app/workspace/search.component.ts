import { Component } from '@angular/core';
import { first } from 'rxjs/operators';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { User, LookingFiles } from '@app/models';
import { AccountService, AlertService, FilterService } from '@app/services';

@Component({ templateUrl: 'search.component.html' })
export class SearchComponent {

    /**
     * @ignore
     */
    form: FormGroup;

    /**
     * @ignore
     */
    user: User;

    /**
     * @ignore
     */
    lookingfiles = null;

    /**
     * @ignore
     */
    files = null;

    /**
     * @ignore
     */
    data: Array<any>;

    /**
     * @ignore
     */
    totalRecords: number;

    /**
     * @ignore
     */
    page: number = 1 ;

    alert = false;

    /**
     * @ignore
     */
    constructor(
        private formBuilder: FormBuilder,
        private accountService: AccountService,
        private filterService: FilterService,
        private alertService: AlertService,
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
        this.alertService.clear();

        this.lookingfiles.positive = positive;
        this.lookingfiles.negative = negative; 
        this.lookingfiles.typefile = type;

        this.data= [];
        this.totalRecords = 0;
        this.page = 1 ;
    }

    /**
     * Search the content requested by the user
     */
    search(){
        this.data= [];
        this.totalRecords = 0;
        this.page = 1 ;
        this.alertService.clear();

        this.lookingfiles.wanted = this.form.value['search'];
        if (this.lookingfiles.wanted == ""){
            this.alertService.warn("You need to specify what looking for");
        }else if(this.lookingfiles.positive == null || this.lookingfiles.negative== null){
            this.alertService.warn("You need to specify the pair of files");
        }else{
            this.filterService.search(this.lookingfiles).subscribe((data) => {
                for(let element of Object.keys(data)){
                    this.data[element]= {id:element, docid: data[element]['docid'], titulo: data[element]['titulo'], abstract: data[element]['abstract'], key_words: data[element]['key_words']}
                };
                this.totalRecords =  Object.keys(data).length;
                if (this.totalRecords == 0){
                    this.alertService.info("No results");
                    this.alert = true;
                }
            },
            error => {
                this.alertService.error(error.error);
                console.log(error.error);
            });
        }
    }

    /**
     * Pagination
     */
    onChangePage(event){
        this.page = event;
    }
  }