var ROUTES_INDEX = {"name":"<root>","kind":"module","className":"AppModule","children":[{"name":"routes","filename":"src/app/app-routing.module.ts","module":"AppRoutingModule","children":[{"path":"","redirectTo":"/home","pathMatch":"full"},{"path":"home","component":"HomeComponent"},{"path":"admin","loadChildren":"usersModule","canActivate":["AuthGuard"],"data":{"roles":["Admin"]}},{"path":"account","loadChildren":"accountModule"},{"path":"workspace","loadChildren":"WorkspaceModule","canActivate":["AuthGuard"]},{"path":"**","redirectTo":""}],"kind":"module"}]}
