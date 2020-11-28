module.exports = function (app, mysql, AES) {
   
    /**
     * GET all users
     */
    app.get("/api/users", (request, response) => {
      mysql.query('SELECT * FROM users', (error, result) => {
          if (error) throw error;
          response.send(result);
      });
    });

    /**
     * GET user : id
     */
    app.get('/api/user/:id', (req, res) => {
      const id = req.params.id;
      mysql.query("SELECT * FROM users WHERE id = ?", id, function (err, result, fields) {
        if (err) res.send(err);
        res.send(result);
        console.log(result);
      });
    });

       /**
     * change param accept : id
     */
    app.get('/api/acceptuser/:id', (req, res) => {
      const id = req.params.id;
      mysql.query("UPDATE users set accept=true WHERE id = ?", id, function (err, result, fields) {
        if (err) res.send(err);
        res.send(result);
        console.log(result);
      });
    });
    
  /**
     * DELETE user : id
     */
    app.delete("/api/user/:id", function (req, res) {
      var id = req.params.id;
      mysql.query('DELETE FROM users WHERE id = ?', id, (error, result) => {
        if (error) throw error;
        res.send(result);
        console.log(result);
      });
    });

    /**
     * POST -> register user
     */
    app.post("/api/user/register", function (req, res) {
       var data = {
        email: req.body.email,
        password: AES.encrypt(req.body.password, req.body.email),
        username: req.body.username,
        first_name: req.body.first_name,
        last_name: req.body.last_name,
        role: req.body.role
      };
      mysql.query("INSERT INTO users SET ?", data, function (err, result) {
        if (err) res.send(err);
        console.log(err);
        res.send(result);
        console.log(result);
      });
    });

    /**
     * POST -> authenticate user
     */
    app.post('/api/users/authenticate', function (req, res) {
      var data = {
        email: req.body.email,
        password: AES.encrypt(req.body.password, req.body.email),
      };
      mysql.query("select * from users where email = ? and password = ?", [data.email, data.password], function (err, result, fields) {
        if (err) res.send(err);
        if (!result.length) res.status(400).send('user not found');
        res.send(result);
        console.log(result);
      });
    });

    /**
     * PUT -> update user
     */
    app.put("/api/user/:id", function (req, res) {
      var id = req.params.id; 
      passwordDB = mysql.query('select password from users where id = ?', id)
      if (req.body.password == passwordDB){
        var data = {
          email: req.body.email,
          password: req.body.password,
          username: req.body.username,
          first_name: req.body.first_name,
          last_name: req.body.last_name,
          role: req.body.role
        };
      }else{
        var data = {
          email: req.body.email,
          password: AES.encrypt(req.body.password, req.body.email),
          username: req.body.username,
          first_name: req.body.first_name,
          last_name: req.body.last_name,
          role: req.body.role
        };
      }
      mysql.query('UPDATE users SET ? WHERE id = ?', [data, id], (error, result) => {
        if (error) res.send(error);
        res.send(result);
        console.log(result);
      });
    });
};
