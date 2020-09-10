module.exports = function (app, mysql) {
   
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
     * DELETE user : id
     */
    app.delete("/api/user/:id", function (req, res) {
      var id = req.params.id;
      mysql.query('DELETE FROM users WHERE id = ?', id, (error, result) => {
        if (error) throw error;
 
        res.send('User deleted.');
    });
});

    /**
     * POST -> register user
     */
    app.post("/api/user/register", function (req, res) {
       var data = {
        email: req.body.email,
        password: req.body.password,
        username: req.body.username,
        first_name: req.body.first_name,
        last_name: req.body.last_name
      };
      mysql.query("INSERT INTO users SET ?", data, function (err, result) {
        if (err) res.send(err);
        console.log(result);
      });
    });

    /**
     * POST -> authenticate user
     */
    app.post('/api/users/authenticate', function (req, res) {
      var data = {
        username: req.body.username,
        password: req.body.password
      };
      mysql.query("select * from users where username = ? and password = ?", [data.username,data.password], function (err, result, fields) {
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
      mysql.query('UPDATE users SET ? WHERE id = ?', [req.body, id], (error, result) => {
        if (error) throw error;
 
        res.send('User updated successfully.');
      });
    });
};
