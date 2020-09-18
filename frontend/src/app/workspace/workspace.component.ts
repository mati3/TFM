import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormGroup, FormControl, Validators} from '@angular/forms';
import { User } from '@app/_models';
import { AccountService, AlertService, FilterService } from '@app/_services';

@Component({ templateUrl: 'workspace.component.html' })
export class WorkspaceComponent {
  myForm = new FormGroup({
    file: new FormControl('', [Validators.required]),
    fileSource: new FormControl('', [Validators.required])
  });
  filesFVS: File[] = [];
  filesFDS: File[] = [];
  filesTIS: File[] = [];
  index: number;
  user: User;

  constructor(private http: HttpClient, private accountService: AccountService) { 
    this.user = this.accountService.userValue;
  }
      
  get f(){
    return this.myForm.controls;
  }
     
  onFileChange(event,typefile: String) {
  
    if (event.target.files.length > 0) {
      const file = event.target.files[0];
      if (typefile === 'filesFVS')
        this.filesFVS.push(file);
      else if (typefile === 'filesFDS')
        this.filesFDS.push(file);
      else if(typefile === 'filesTIS')
        this.filesTIS.push(file);
      this.myForm.patchValue({
        fileSource: file
      });
    }
  }
  upload(file,typefile: String){
    const formData = new FormData();
    formData.append('file', file);
    file.invalid = true
    this.http.post(`http://localhost:5000/upload/${this.user.email}/${typefile}`, formData)
      .subscribe(res => {
        console.log(res);
      })
  }   
 
  remove(file,typefile: String){
    if (typefile === 'filesFVS'){
      this.index = this.filesFVS.indexOf(file);
      this.filesFVS.splice(this.index,1);
    }else if (typefile === 'filesFDS'){
      this.index = this.filesFDS.indexOf(file);
      this.filesFDS.splice(this.index,1);
    }else if(typefile === 'filesTIS'){
      this.index = this.filesTIS.indexOf(file);
      this.filesTIS.splice(this.index,1);
    }
    const formData = new FormData();
    formData.append('file', file);
    this.http.post(`http://localhost:5000/removefile/${this.user.email}`, formData)
      .subscribe(res => {
        console.log(res);
      })
  }
}