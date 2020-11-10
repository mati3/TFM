import { Component } from '@angular/core';
import { first } from 'rxjs/operators';
import { User, LookingFiles, Filter, Metric } from '@app/models';
import { AccountService, FilterService } from '@app/services';

@Component({ templateUrl: 'filter.component.html' })
export class FilterComponent {

  /**
   * @ignore
   */
  user: User;

  /**
   * @ignore
   */
  files = null;

  /**
   * @ignore
   */
  lookingfiles = null;

  /**
   * @ignore
   */
  sum: number;

  /**
   * @ignore
   */
  filter: Filter;

  /**
   * @ignore
   */
  query = null;

  /**
   * @ignore
   */
  metricsFVS = [];

  /**
   * @ignore
   */
  metricsFDS = [];
  
  /**
   * @ignore
   */
  metric = null;

  /**
   * @ignore
   */
  loading = false;

  /**
   * @ignore
   */
  loadand = true;

  /**
   * @ignore
   */
  loadmetric = false;

  /**
   * @ignore
   */
  loadfile = false;

  /**
   * @ignore
   */
  loadfilter = false;

  /**
   * @ignore
   */
  loadnum = false;

  /**
   * @ignore
   */
  loadapply = false;

  /**
   * @ignore
   */
  constructor(
      private accountService: AccountService,
      private filterService: FilterService
      ) {
      this.user = this.accountService.userValue;
      this.lookingfiles = new LookingFiles(this.user.email);
      this.filter = new Filter();
  }

  /**
   * Select a filter
   * 
   * @param {Event} event - Selected filter
   */
  changefilter(event){
    this.filter.typefilter = event.target.value;
    this.loadfilter = true;
  }

  /**
   * Choose the number of terms for the query
   * 
   * @param {Event} event - Number of terms
   */
  termNumber(event){
    this.filter.sum = event.target.value;
    this.loadnum = true;
  }

  /**
   * Retrieves the names of the files associated with a user from the database
   */
  ngOnInit() {
      this.filterService.getAllFiles(this.user.email)
          .pipe(first())
          .subscribe(files => this.files = files);
  }

  /**
   * Select pair of files TIS
   * 
   * @param {String} positive - File positive
   * @param {String} negative - File negative
   */
  select(positive, negative){
    this.lookingfiles.positive = positive;
    this.lookingfiles.negative = negative; 
    this.lookingfiles.typefile = 'fileTIS';
    this.filterService.selectTIS(this.lookingfiles)
      .pipe(first())
      .subscribe(
        x => {
          this.filter.terms_freqs_positive = x['terms_freqs_positive'];
          this.filter.terms_freqs_negative = x['terms_freqs_negative'];
      });
    this.loadfile = true;
  }

  /**
   * With the pair of TIS files selected, the filter chosen and the number of terms determined (X), 
   * choose the first X most relevant terms
   */
  onSubmit(){
    this.loadapply = true;
    this.loadand = true;
    this.loading = false;
    this.filter.email = this.user.email;

    this.filterService.selectFilter(this.filter)
      .pipe(first())
      .subscribe(x => this.query = x);
    
    this.metricsFVS = [];
    this.metricsFDS = [];
  }

  /**
   * Add the boolean AND operator to the query
   */
  andOperator(){
    this.loadand = true;
    for (let i = 0; i < (this.filter.sum - 1); i++){
        this.query[i] = this.query[i] + " AND ";
        this.lookingfiles.wanted += this.query[i];
    }
    this.lookingfiles.wanted += this.query[this.filter.sum-1];
    this.loadand = false;  
  }

  /**
   * Apply the selected filter on the FVS file pair
   */
  applyFilterFVS(){
    if (this.lookingfiles.wanted == ""){
      this.query.forEach(element => {
        this.lookingfiles.wanted += element + " ";
      });
    }
    this.lookingfiles.typefile = 'filesFVS';
    this.filterService.applyFilter(this.lookingfiles).subscribe((data) => {
      this.metricsFVS = [];
      this.metric = [];
      for(let element of Object.keys(data)){
        this.metric = [];
        for(let des in data[element]){
          this.metric.push(new Metric(element,des,data[element][des]));
        }
        this.metricsFVS.push(this.metric);
      };
    });
    this.lookingfiles.wanted = "";
    this.loadmetric = true;
  } 

  /**
   * Apply the selected filter on the FDS file pair
   */
  applyFilterFDS(){
    if (this.lookingfiles.wanted == ""){
      this.query.forEach(element => {
        this.lookingfiles.wanted += element + " ";
      });
    }
    this.lookingfiles.typefile = 'filesFDS';
    this.filterService.applyFilter(this.lookingfiles).subscribe((data) => {
      this.metricsFDS = [];
      this.metric = [];
      for(let element of Object.keys(data)){
        this.metric = [];
        for(let des in data[element]){
          this.metric.push(new Metric(element,des,data[element][des]));
        }
        this.metricsFDS.push(this.metric);
      };
    });
    this.lookingfiles.wanted = "";
    this.loadmetric = true;
  }

}