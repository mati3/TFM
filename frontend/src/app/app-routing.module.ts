import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { TranslateService } from '@ngx-translate/core';
import { HomeComponent } from './home';
import { AuthGuard } from './_helpers';
import { Role } from './_models';

const accountModule = () => import('./account/account.module').then(x => x.AccountModule);
const usersModule = () => import('./admin/users.module').then(x => x.UsersModule);
const WorkspaceModule = () => import('./workspace/workspace.module').then(x => x.WorkspaceModule);

const routes: Routes = [
    { path: '', redirectTo: '/home', pathMatch: 'full' },
    { path: 'home', component: HomeComponent },
    { path: 'admin', loadChildren: usersModule, canActivate: [AuthGuard], data: { roles: [Role.Admin] }  },
    { path: 'account', loadChildren: accountModule, data: { currentLang: TranslateService } },
    { path: 'workspace', loadChildren: WorkspaceModule, canActivate: [AuthGuard] },

    // otherwise redirect to home
    { path: '**', redirectTo: '' }
];

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
})
export class AppRoutingModule { } 