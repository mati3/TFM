import { Component } from '@angular/core';
import { first } from 'rxjs/operators';

import { User } from '@app/_models';
import { AccountService, AlertService, FilterService } from '@app/_services';

@Component({ templateUrl: 'filter.component.html' })
export class FilterComponent {

  user: User;
  files = null;

  constructor(
      private accountService: AccountService,
      private filterService: FilterService,
      private alertService: AlertService
      ) {
      this.user = this.accountService.userValue;
  }

  ngOnInit() {
      this.filterService.getAllFiles(this.user.email)
          .pipe(first())
          .subscribe(files => this.files = files);
  }
}