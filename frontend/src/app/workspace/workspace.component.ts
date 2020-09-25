import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormGroup, FormControl, Validators} from '@angular/forms';
import { User } from '@app/_models';
import { AccountService, FilterService } from '@app/_services';
import { first } from 'rxjs/operators';

@Component({ templateUrl: 'workspace.component.html' })
export class WorkspaceComponent {
  myForm = new FormGroup({
    filepositive: new FormControl('', [Validators.required]),
    filenegative: new FormControl('', [Validators.required])
  });
  filesFVS = [];
  filesFDS = [];
  filesTIS = [];
  filepositive: File ;
  myfiles = null;
  typefile: String;
  index: number;
  user: User;

  constructor(private http: HttpClient, 
    private accountService: AccountService,
    private filterService: FilterService) { 
    this.user = this.accountService.userValue;
  }
      
  get f(){
    return this.myForm.controls;
  }
  //onInit hay que poner que lea en la base de datos
  ngOnInit() {
    this.myForm.controls.filenegative.disable();
    this.filterService.getAllFiles(this.user.email)
      .pipe(first())
      .subscribe(files => this.myfiles = files);
  }
     
  onFileChange(event,typefile: String) {
    this.myForm.controls.filenegative.enable();
    if (event.target.files.length > 0 && this.myForm.valid) {
      const file = event.target.files[0];
      if (typefile === 'filesFVS'){
        this.filesFVS.push({'filenegative':file,'filepositive':this.filepositive});
      } else if (typefile === 'filesFDS'){
        this.filesFDS.push({'filenegative':file,'filepositive':this.filepositive});
      } else if(typefile === 'filesTIS'){
        this.filesTIS.push({'filenegative':file,'filepositive':this.filepositive});
      }
      // si ya tenemos filepositive y negative, reseteamos
      if (this.myForm.valid){
        this.myForm.reset();
        this.myForm.controls.filenegative.disable();
      }
      this.filepositive = null;
    }else if(this.myForm.invalid  && this.myForm.controls.filepositive.valid){
      this.filepositive = event.target.files[0];
      //this.myForm.controls.filenegative.enable();
    }
  }

  clear(item,typefile: String){
    if (typefile === 'filesFVS'){
      this.index = this.filesFVS.indexOf(item);
      this.filesFVS.splice(this.index,1);
    }else if (typefile === 'filesFDS'){
      this.index = this.filesFDS.indexOf(item);
      this.filesFDS.splice(this.index,1);
    }else if(typefile === 'filesTIS'){
      this.index = this.filesTIS.indexOf(item);
      this.filesTIS.splice(this.index,1);
    }
  }
  
  upload(item,typefile: String){
    const formData = new FormData();
    formData.append('filepositive', item.filepositive);
    formData.append('filenegative', item.filenegative);
    item.invalid = true
    this.filterService.upload(this.user.email, typefile, formData);
  }   

  filetype(typefile: String){
    this.typefile = typefile;
  }
  
  removeindex(){
    if (this.typefile === 'filesFVS'){
      this.filesFVS = [];
    }else if (this.typefile === 'filesFDS'){
      this.filesFDS = [];
    }else if(this.typefile === 'filesTIS'){
      this.filesTIS = [];
    }
    this.filterService.deleteIndex(this.user.email, this.typefile);
  }
}