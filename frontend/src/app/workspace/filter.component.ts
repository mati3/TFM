import { Component } from '@angular/core';
import { first } from 'rxjs/operators';
import { User, LookingFiles, Filter, Metric } from '@app/models';
import { AccountService, FilterService } from '@app/services';

@Component({ templateUrl: 'filter.component.html' })
export class FilterComponent {

  user: User;
  files = null;
  pos = null;
  neg = null;
  lookingfiles = null;
  typefilter = "";
  sum: number;
  filter: Filter;
  loading = false;
  query = null;
  wanted = "";
  andleng = 0;
  loadand = true;
  loadmetric = false;
  metricsFVS = [];
  metricsFDS = [];
  metric = null;

  constructor(
      private accountService: AccountService,
      private filterService: FilterService,
      ) {
      this.user = this.accountService.userValue;
      this.lookingfiles = new LookingFiles(this.user);
      this.filter = new Filter();
  }

  changefilter(event){
    this.filter.typefilter = event.target.value;
    console.log(this.filter.typefilter);
    // comprobar que este filtro existe en filter enum
  }

  termNumber(event){
    this.filter.sum = event.target.value;
    console.log(this.filter.sum);
  }

  ngOnInit() {
      this.filterService.getAllFiles(this.user.email)
          .pipe(first())
          .subscribe(files => this.files = files);
  }

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
  }

  onSubmit(){
    this.loading = true;
    this.loadand = true;
    if (this.filter.typefilter == null){
      console.log("tienes que elegir un filtro");
    }
    else if(this.filter.sum == null){// no numeros negativos, minimo 1
      console.log(" elige la cantidad de terminos a tratar ");
    }
    else if ((this.lookingfiles.positive == null) || (this.lookingfiles.negative == null)){
      console.log(" has de seleccionar el par de archivos TIS ");
    }
    else {
      this.loading = false;
      this.filter.email = this.user.email;
      console.log(this.filter)
      this.filterService.selectFilter(this.filter)
      .pipe(first())
      .subscribe(x => this.query = x);
      this.andleng = this.filter.sum - 1; //cantidad AND
    }
  }

  andOperator(){
    this.loadand = true;
    this.andleng = this.filter.sum - 1; //cantidad AND
    for (let i = 0; i < this.andleng; i++){
      console.log(this.query[i]);
        this.query[i] = this.query[i] + " AND ";
        this.loadand = false;      
    }
  }

  applyFilterFVS(){
    this.query.forEach(element => {
      this.wanted += element + " ";
    });
    console.log(this.wanted)
    // PROBISIONAL, para ver los archivos buscados.
    this.lookingfiles.wanted = this.wanted;
    this.wanted = "";
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
    this.loadmetric = true;
  } 

  applyFilterFDS(){
    this.query.forEach(element => {
      this.wanted += element + " ";
    });
    console.log(this.wanted)
    // PROBISIONAL, para ver los archivos buscados.
    this.lookingfiles.wanted = this.wanted;
    this.wanted = "";
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
    this.loadmetric = true;
  }

}