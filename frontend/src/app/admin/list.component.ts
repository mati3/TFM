import { Component, OnInit } from '@angular/core';
import { first } from 'rxjs/operators';
import { AccountService, AlertService, FilterService } from '@app/services';
import { Router, ActivatedRoute } from '@angular/router';

@Component({ templateUrl: 'list.component.html' })
export class ListComponent implements OnInit {
    users = null;
    loading = false;

    constructor(private accountService: AccountService,
        private route: ActivatedRoute,
        private router: Router,
        private alertService: AlertService,
        private filterService: FilterService) {
        }

    ngOnInit() {
        this.accountService.getAll()
            .pipe(first())
            .subscribe(users => this.users = users);
    }

    deleteUser(id: string) {
        const user = this.users.find(x => x.id === id);
        user.isDeleting = true;
        this.accountService.delete(id)
            .pipe(first())
            .subscribe(() => {
                this.users = this.users.filter(x => x.id !== id); 
            },
            error => {
                this.alertService.error(error);
            }); 
        this.filterService.deleteUser(user.email)
            .pipe(first())
            .subscribe();  
    }

    acceptUser(id: string) {
        this.loading = true;
        const user = this.users.find(x => x.id === id);
        user.isSuccess = user.accept = true;
        this.accountService.accept(id)
            .pipe(first())
            .subscribe(
                data => {
                    this.alertService.success('Update successful', { keepAfterRouteChange: true });
                    this.router.navigate(['..', { relativeTo: this.route }]);
                }/*,
                error => {
                    this.alertService.error(error);
                    this.isSuccess = false;
                }*/);
        this.filterService.addUser(user.email)
            .pipe(first())
            .subscribe(
                error => {
                this.alertService.error("");
                user.isSuccess = false;
            });        
        user.isSuccess = user.accept = true;
    }
}
