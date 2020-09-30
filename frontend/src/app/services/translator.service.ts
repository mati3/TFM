import { Injectable } from '@angular/core';
import { TranslateService } from '@ngx-translate/core';

@Injectable({ providedIn: 'root' })
export class TranslatorService {

    currentLang = 'English';

    constructor(public translate: TranslateService) {
        this.translate.addLangs(['English', 'Spanish']);
        this.translate.setDefaultLang('English');
    }    

    selectLanguage(lang: string) {
        this.currentLang = lang ;
        return this.translate.use(lang);
    }

    getLangs(){
        return this.translate.getLangs();
    }

    getCurrentLang(){
        return this.currentLang;
    }

}