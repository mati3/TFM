import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { first } from 'rxjs/operators';

import { AccountService, AlertService } from '@app/services';

@Component({ templateUrl: 'register.component.html' })
export class RegisterComponent implements OnInit {
    /**
     * @ignore
     */
    form: FormGroup;

    /**
     * @ignore
     */
    loading = false;

    /**
     * @ignore
     */
    submitted = false;

    /**
     * @ignore
     */
    constructor(
        private formBuilder: FormBuilder,
        private route: ActivatedRoute,
        private router: Router,
        private accountService: AccountService,
        private alertService: AlertService
    ) { }

    /**
     * Validate the user variables
     */
    ngOnInit() {
        this.form = this.formBuilder.group({
            first_name: ['', [Validators.required, Validators.maxLength(50)]],
            last_name: ['', [Validators.required, Validators.maxLength(50)]],
            username: ['', [Validators.required, Validators.maxLength(50)]],
            email: ['', [Validators.required, Validators.maxLength(25), Validators.pattern("^[a-z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,4}$")]],
            password: ['', [Validators.required, Validators.minLength(6), Validators.maxLength(50)]]
        });
    }

    /**
     * Get an access to form fields
     * 
     * @return {Form} - Form controls
     */
    get f() { return this.form.controls; }

    /**
     * Register an user
     * 
     * @return {String} - If an error occurs, explanation of what happened
     */
    onSubmit() {
        this.submitted = true;
        this.alertService.clear();
        if (this.form.invalid) {
            return this.alertService.error("Invalid user");
        }

        this.loading = true;
        this.accountService.register(this.form.value)
            .pipe(first())
            .subscribe(
                data => {
                    this.alertService.success('Registration successful', { keepAfterRouteChange: true });
                    this.router.navigate(['../login'], { relativeTo: this.route });
                },
                error => {
                    this.alertService.error(error);
                    this.loading = false;
                });
    }
}