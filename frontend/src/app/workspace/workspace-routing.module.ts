import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { WorkspaceComponent } from './workspace.component';

const routes: Routes = [
    {
        path: '', component: WorkspaceComponent,
        children: []
    }
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class WorkspaceRoutingModule { }