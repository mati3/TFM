import { Component } from '@angular/core';
import { first } from 'rxjs/operators';

import { User } from '@app/_models';
import { AccountService, AlertService, FilterService } from '@app/_services';

@Component({ templateUrl: 'filter.component.html' })
export class FilterComponent {

  user: User;
  files = null;
  users = null;

  constructor(
      private accountService: AccountService,
      private filterService: FilterService,
      private alertService: AlertService
      ) {
      this.user = this.accountService.userValue;
  }

  ngOnInit() {
      this.filterService.getAll()
          .pipe(first())
          .subscribe(users => this.users = users);
      this.filterService.getAllFilesIndex(this.user.email)
          .pipe(first())
          .subscribe(files => this.files = files);
          console.log(this.files);
  }
}