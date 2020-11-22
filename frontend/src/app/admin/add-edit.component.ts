﻿import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { first } from 'rxjs/operators';

import { AccountService, AlertService } from '@app/services';

@Component({ templateUrl: 'add-edit.component.html' })
export class AddEditComponent implements OnInit {
    form: FormGroup;
    id: string;
    isAddMode: boolean;
    loading = false;
    submitted = false;

    constructor(
        private formBuilder: FormBuilder,
        private route: ActivatedRoute,
        private router: Router,
        private accountService: AccountService,
        private alertService: AlertService
    ) {}

    ngOnInit() {
        this.id = this.route.snapshot.params['id'];
        this.isAddMode = !this.id;
        
        // password not required in edit mode
        const passwordValidators = [Validators.minLength(6), Validators.maxLength(50)];
        if (this.isAddMode) {
            passwordValidators.push(Validators.required);
        }

        this.form = this.formBuilder.group({
            first_name: ['', [Validators.required, Validators.maxLength(50)]],
            last_name: ['', [Validators.required, Validators.maxLength(50)]],
            username: ['', [Validators.required, Validators.maxLength(25)]],
            email: ['', [Validators.required, Validators.maxLength(25), Validators.pattern("^[a-z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,4}$")]],
            password: ['', passwordValidators],
            role:['']
        });

        if (!this.isAddMode) {
            this.accountService.getById(this.id)
                .pipe(first())
                .subscribe(x => {
                    this.form = this.formBuilder.group({
                        first_name: [x[0].first_name, [Validators.required, Validators.maxLength(50)]],
                        last_name: [x[0].last_name, [Validators.required, Validators.maxLength(50)]],
                        username: [x[0].username, [Validators.required, Validators.maxLength(50)]],
                        email: [x[0].email, [Validators.required, Validators.maxLength(25), Validators.pattern("^[a-z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,4}$")]],
                        password: [x[0].password, passwordValidators],
                        role: [x[0].role]
                    });
                });
        }
    }

    // convenience getter for easy access to form fields
    get f() { return this.form.controls; }

    onSubmit() {
        this.submitted = true;

        // reset alerts on submit
        this.alertService.clear();

        // stop here if form is invalid
        if (this.form.invalid) {
            return;
        }

        this.loading = true;
        if (this.isAddMode) {
            this.createUser();
        } else {
            this.updateUser();
        }
    }

    private createUser() {
        if (this.form.value.role == ""){
            this.form.value.role = "User"
        }else if (this.form.value.role){
            this.form.value.role = "Admin"
        }

        this.accountService.register(this.form.value)
            .pipe(first())
            .subscribe(
                data => {
                    if (data['errno'] == 1062){
                        this.alertService.error('Existing user');
                        this.loading = false;
                    }else{
                        this.alertService.success('User added successfully', { keepAfterRouteChange: true });
                        this.router.navigate(['.', { relativeTo: this.route }]);
                    }
                },
                error => {
                    this.alertService.error(error.error);
                    this.loading = false;
                });
                this.form.value.role == 0;
    }

    private updateUser() {
        if (this.form.value.role == ""){
            this.form.value.role = "User"
        }else if (this.form.value.role){
            this.form.value.role = "Admin"
        }

        this.accountService.update(this.id, this.form.value)
            .pipe(first())
            .subscribe(
                data => {
                    if (data['errno'] == 1062){
                        this.alertService.error('Existing user');
                        this.loading = false;
                    }else{
                        this.alertService.success('Update successful', { keepAfterRouteChange: true });
                        this.router.navigate(['..', { relativeTo: this.route }]);
                    }
                },
                error => {
                    this.alertService.error(error.error.text);
                    this.loading = false;
                });
    }
}