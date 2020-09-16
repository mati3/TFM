import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { WorkspaceComponent } from './workspace.component';
import { SearchComponent } from './search.component';
import { FilterComponent } from './filter.component';

const routes: Routes = [
    { path: '', component: WorkspaceComponent  },
    { path: 'search', component: SearchComponent },
    { path: 'filter', component: FilterComponent }
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class WorkspaceRoutingModule { }