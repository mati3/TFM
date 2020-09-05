import { NgModule } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { TranslateLoader, TranslateModule } from '@ngx-translate/core';
import { TranslateHttpLoader } from '@ngx-translate/http-loader';
import { HttpClient } from '@angular/common/http';

import { AccountRoutingModule } from './account-routing.module';
import { LoginComponent } from './login.component';
import { RegisterComponent } from './register.component';
import { ProfileComponent } from './profile.component';


@NgModule({
  imports: [
      CommonModule,
      ReactiveFormsModule,
      AccountRoutingModule,
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
      LoginComponent,
      RegisterComponent,
      ProfileComponent
  ]
})
export class AccountModule { }

export function httpTranslateLoader(http: HttpClient) {
    return new TranslateHttpLoader(http);
  }