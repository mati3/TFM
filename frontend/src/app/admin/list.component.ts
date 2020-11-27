import { Component, OnInit } from '@angular/core';
import { first } from 'rxjs/operators';
import { AccountService, AlertService, FilterService } from '@app/services';
import { Router, ActivatedRoute } from '@angular/router';

@Component({ templateUrl: 'list.component.html' })
export class ListComponent implements OnInit {
    /**
     * @ignore
     */
    users = null;

    /**
     * @ignore
     */
    loading = false;

    /**
     * @ignore
     */
    constructor(private accountService: AccountService,
        private route: ActivatedRoute,
        private router: Router,
        private alertService: AlertService,
        private filterService: FilterService) {
        }

    /**
     * Get a list of all users
     */
    ngOnInit() {
        this.accountService.getAll()
            .pipe(first())
            .subscribe(users => this.users = users);
    }

    /**
     * Delete an user
     * 
     * @param {String} id -  User identification to be deleted
     */
    deleteUser(id: string) {
        const user = this.users.find(x => x.id === id);
        user.isDeleting = true;
        this.accountService.delete(id)
            .pipe(first())
            .subscribe(() => {
                this.users = this.users.filter(x => x.id !== id); 
                this.alertService.info('User deleted');
            },
            error => {
                this.alertService.error(error);
            }); 
        this.filterService.deleteUser(user.email)
            .pipe(first())
            .subscribe();  
    }

    /**
     * Accept an user
     * 
     * @param {String} id -  User identification to be accept
     */
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
