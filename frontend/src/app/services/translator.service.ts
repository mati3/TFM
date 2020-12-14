import { Injectable } from '@angular/core';
import { TranslateService } from '@ngx-translate/core';

@Injectable({ providedIn: 'root' })
export class TranslatorService {

    /**
     * Current language
     */
    currentLang = 'English';

    /**
     * @ignore
     */
    constructor(public translate: TranslateService) {
        this.translate.addLangs(['English', 'Spanish']);
        this.translate.setDefaultLang('English');
    }    

    /**
     * Select language
     * 
     * @param {String} lang - Language
     */
    selectLanguage(lang: string) {
        this.currentLang = lang ;
        return this.translate.use(lang);
    }

    /**
     * Get language
     */
    getLangs(){
        return this.translate.getLangs();
    }

    /**
     * Get current language
     */
    getCurrentLang(){
        return this.currentLang;
    }

}