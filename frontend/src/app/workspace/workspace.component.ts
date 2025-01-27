import { Component } from '@angular/core';
import { FormBuilder, FormGroup, FormControl, Validators} from '@angular/forms';
import { User, LookingFiles } from '@app/models';
import { AccountService, FilterService, AlertService } from '@app/services';
import { first } from 'rxjs/operators';

@Component({ templateUrl: 'workspace.component.html' })
export class WorkspaceComponent {
  /**
   * @ignore
   */
  myForm = new FormGroup({
    filepositive: new FormControl('', [Validators.required]),
    filenegative: new FormControl('', [Validators.required])
  });

  /**
   * @ignore
   */
  filesFVS = [];

  /**
   * @ignore
   */
  filesFDS = [];

  /**
   * @ignore
   */
  filesTIS = [];

  /**
   * @ignore
   */
  filepositive: File ;

  /**
   * @ignore
   */
  myfiles = null;

  /**
   * @ignore
   */
  typefile: String;

  /**
   * @ignore
   */
  index: number;

  /**
   * @ignore
   */
  user: User;

  /**
   * @ignore
   */
  loadfilepositiveFVS = false;

  /**
   * @ignore
   */
  loadfilepositiveFDS = false;

  /**
   * @ignore
   */
  loadfilepositiveTIS = false;

  /**
   * @ignore
   */
  lookingfiles = null;

  /**
   * @ignore
   */
  constructor( 
    private accountService: AccountService,
    private alert: AlertService,
    private filterService: FilterService) { 
      this.user = this.accountService.userValue;
      this.lookingfiles = new LookingFiles(this.user.email);
  }
  
  /**
   * Form.controls
   */
  get f(){
    return this.myForm.controls;
  }

  /**
   * Retrieves the names of the files associated with a user from the database
   */
  ngOnInit() {
    this.myForm.controls.filenegative.disable();
    this.filterService.getAllFiles(this.user.email)
      .pipe(first())
      .subscribe(files => this.myfiles = files);
  }
     
  /**
   * Enter a pair of files (positive and negative) selected by the user
   * 
   * @param {Event} event - Event, pick up a file
   * @param {String} typefile - Type of file
   */
  onFileChange(event,typefile: String) {

    if (event.target.files[0].type != 'text/plain'){
      this.alert.error("Only text files (.txt) are supported");
    } else if (event.target.files[0].size <=1 ){
      this.alert.error("File is empty");
    }else{
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
        this.loadfilepositiveFVS = false;
        this.loadfilepositiveFDS = false;
        this.loadfilepositiveTIS = false;
      }else if(this.myForm.invalid  && this.myForm.controls.filepositive.valid){
        this.filepositive = event.target.files[0];
        this.myForm.controls.filenegative.enable();
        if (typefile === 'filesFVS'){
          this.loadfilepositiveFVS = true;
          this.loadfilepositiveFDS = false;
          this.loadfilepositiveTIS = false;
        } else if (typefile === 'filesFDS'){
          this.loadfilepositiveFDS = true;
          this.loadfilepositiveFVS = false;
          this.loadfilepositiveTIS = false;
        } else if(typefile === 'filesTIS'){
          this.loadfilepositiveTIS = true;
          this.loadfilepositiveFDS = false;
          this.loadfilepositiveFVS = false;
        }
      }
    }
  }

  /**
   * Delete (clean) a couple of files before putting them in the database
   * 
   * @param {Files} item - Pair of files, positive and negative
   * @param {String} typefile - Type of file
   */
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
  
  /**
   * Enter and index the selected pair of files in the database
   * 
   * @param {Files} item - Pair of files, positive and negative
   * @param {String} typefile - Type of file
   */
  upload(item,typefile: string){
    const formData = new FormData();
    formData.append('filepositive', item.filepositive);
    formData.append('filenegative', item.filenegative);
    formData.append('email', this.user.email);
    formData.append('typefile', typefile);
    item.invalid = true
    // aqui necesito usar formData para que envie el File. No usar lookingfiles,  envia un dic.
    this.filterService.upload(formData);
  }   

  /**
   * Select the type of file to be processed
   * 
   * @param {String} typefile - Type of file
   */
  filetype(typefile: String){
    this.typefile = typefile;
  }
  
  /**
   * Delete all files within the selected filetype group
   */
  removeindex(){
    if (this.typefile === 'filesFVS'){
      this.filesFVS = [];
      this.myfiles.filesFVS = null
    }else if (this.typefile === 'filesFDS'){
      this.filesFDS = [];
      this.myfiles.filesFDS = null
    }else if(this.typefile === 'filesTIS'){
      this.filesTIS = [];
      this.myfiles.filesTIS = null;
    }
    this.filterService.deleteIndex(this.user.email, this.typefile);
  }
}