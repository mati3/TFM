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
        //console.log(this.form.value)
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
        //this.items = Array(150).fill(0).map((x, i) => ({ id: (i + 1), name: `Item ${i + 1}`}));
        //for(let element of this.result){
          //  this.items[element.index]= {id:element.index, titulo: element['titulo'], abstract: element.abstract, golden_words: element.golden_words}
        //};
        this.filterService.search(this.lookingfiles).subscribe((data) => {
            //console.log(data);
            //this.data = data;
            //this.totalRecords = data.length;
            for(let element of Object.keys(data)){
                this.data[element]= {id:element, titulo: data[element]['titulo'], abstract: data[element]['abstract'], golden_words: data[element]['golden_words']}
                //console.log(data[element]['titulo'])
            };
            this.totalRecords =  Object.keys(data).length;
        });
        console.log(this.data);
    }

    onChangePage(event){
        console.log(event);
        this.page = event;
    }
  }