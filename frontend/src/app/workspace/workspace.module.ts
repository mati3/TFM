import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { TranslateLoader, TranslateModule } from '@ngx-translate/core';
import { TranslateHttpLoader } from '@ngx-translate/http-loader';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { FileUploadModule } from "ng2-file-upload";
import { ngfModule } from "angular-file";
import { BrowserModule } from '@angular/platform-browser';


import { WorkspaceRoutingModule } from './workspace-routing.module';
import { WorkspaceComponent } from './workspace.component';
import { SearchComponent } from './search.component';
import { FilterComponent } from './filter.component';

@NgModule({
    imports: [
        CommonModule,
        ReactiveFormsModule,
        FileUploadModule,
        FormsModule,
        HttpClientModule,
        ngfModule,
        WorkspaceRoutingModule,
        TranslateModule.forChild({ 
          useDefaultLang: true, 
          isolate: false, 
          loader: {
            provide: TranslateLoader,
            useFactory: httpTranslateLoader,
            deps: [HttpClient]
          } 
        })
    ],
    declarations: [
        WorkspaceComponent,
        SearchComponent,
        FilterComponent
    ]
})
export class WorkspaceModule { }

export function httpTranslateLoader(http: HttpClient) {
    return new TranslateHttpLoader(http);
  }