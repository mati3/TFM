import { NgModule } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { TranslateLoader, TranslateModule } from '@ngx-translate/core';
import { TranslateHttpLoader } from '@ngx-translate/http-loader';
import { HttpClient } from '@angular/common/http';

import { WorkspaceRoutingModule } from './workspace-routing.module';
import { WorkspaceComponent } from './workspace.component';

@NgModule({
    imports: [
        CommonModule,
        ReactiveFormsModule,
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
        WorkspaceComponent
    ]
})
export class WorkspaceModule { }

export function httpTranslateLoader(http: HttpClient) {
    return new TranslateHttpLoader(http);
  }