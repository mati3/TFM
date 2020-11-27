import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { first } from 'rxjs/operators';

import { AccountService, AlertService } from '@app/services';

@Component({ templateUrl: 'login.component.html' })
export class LoginComponent implements OnInit {
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
    returnUrl: string;

    /**
     * @ignore
     */
    constructor(
        private formBuilder: FormBuilder,
        private route: ActivatedRoute,
        private router: Router,
        private accountService: AccountService,
        private alertService: AlertService
    ) {
        // redirect to home if already logged in
        if (this.accountService.userValue) {
            this.router.navigate(['/']);
        }
     }

    /**
     * Validate the email and password variables
     */
    ngOnInit() {
        this.form = this.formBuilder.group({
            email: ['', Validators.required],
            password: ['', Validators.required]
        });

        // get return url from route parameters or default to '/'
        this.returnUrl = this.route.snapshot.queryParams['returnUrl'] || '/';
    }

    /**
     * Get an access to form fields
     * 
     * @return {Form} - Form controls
     */
    get f() { return this.form.controls; }

    /**
     * Authenticate an user
     * 
     * @return {String} - If an error occurs, explanation of what happened
     */
    onSubmit() {
        this.submitted = true;
        this.alertService.clear();
        if (this.form.invalid) {
            return this.alertService.error("Invalid email or password");
        }

        this.loading = true;
        this.accountService.login(this.f.email.value, this.f.password.value)
            .pipe(first())
            .subscribe(
                user =>{
                    if (user == null){
                        this.alertService.error("User not accepted");
                        this.loading = false;
                    }else {
                        this.router.navigate([this.returnUrl]);
                    }
                },
                error => {
                    this.alertService.error("Wrong email or password");
                    this.loading = false;
                });
    }
}