﻿﻿import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { first } from 'rxjs/operators';

import { AccountService, AlertService } from '@app/services';

@Component({ templateUrl: 'add-edit.component.html' })
export class AddEditComponent implements OnInit {
    /**
     * @ignore
     */
    form: FormGroup;

    /**
     * @ignore
     */
    id: string;

    /**
     * @ignore
     */
    isAddMode: boolean;

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
    checked = false;

    /**
     * @ignore
     */
    constructor(
        private formBuilder: FormBuilder,
        private route: ActivatedRoute,
        private router: Router,
        private accountService: AccountService,
        private alertService: AlertService
    ) {}

    /**
     * Validate the user variables
     */
    ngOnInit() {
        this.id = this.route.snapshot.params['id'];
        this.isAddMode = !this.id;
        
        // password not required in edit mode
        const passwordValidators = [Validators.minLength(6), Validators.maxLength(15)];
        if (this.isAddMode) {
            passwordValidators.push(Validators.required);
        }

        this.form = this.formBuilder.group({
            first_name: ['', [Validators.required, Validators.maxLength(50)]],
            last_name: ['', [Validators.required, Validators.maxLength(50)]],
            username: ['', [Validators.required, Validators.maxLength(50)]],
            email: ['', [Validators.required, Validators.maxLength(25), Validators.pattern("^[a-z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,4}$")]],
            password: ['', passwordValidators],
            last_password: [''],
            role:['User']
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
                        password: [x[0].password, [Validators.minLength(6), Validators.maxLength(50)]],
                        last_password: [x[0].password],
                        role: [x[0].role]
                    });
                    if (this.form.value.role == "Admin"){
                        this.checked = true;
                    }
                });
        }
    }

    /**
     * Get an access to form fields
     * 
     * @return {Form} - Form controls
     */
    get f() { return this.form.controls; }

    /**
     * Edit or Add an user
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
        if (this.isAddMode) {
            this.createUser();
        } else {
            this.updateUser();
        }
    }

    /**
     * Change user role
     */
    changeUser(event){
        console.log(event.currentTarget.checked);
        if(event.currentTarget.checked){
            this.form.value.role = "Admin";
        }else{
            this.form.value.role = "User";
        }
        //this.form.value.role = event.target.value;
    }

    /**
     * Add an user
     */
    private createUser() {

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
    }

    /**
     * Edit an user
     */
    private updateUser() {
        console.log(this.form.value);
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