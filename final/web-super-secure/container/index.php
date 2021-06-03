<?php
ini_set('display_errors', 0);

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $users = [
        'l337haxx00r' => '$2y$10$FXt6xgp7jgkPH4qiFf1Fx.oIg3ZUWFj8jf3g1zwCDrJzK/vXQy/a6',
        'jeffbezos89' => '$2y$10$8jKNL0FZgsqqXzxC6akQxe0Y9Psu94kQDPfOyj8os986SyXNnIFfa',
    ];
    $Array = $_POST;

    if (password_verify($Array['password'], $$users[$Array['username']])) {
        $success = true;
    } else {
        $success = false;
    }
}
?>

<!doctype html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-eOJMYsd53ii+scO/bJGFsiCZc+5NDVN2yr8+0RDqr0Ql0h+rP48ckxlpbzKgwra6" crossorigin="anonymous">

    <title>Login</title>
</head>

<body>
    <div class="container mt-3">
        <?php if ($_SERVER['REQUEST_METHOD'] === 'POST') { ?>
            <?php if ($success) { ?>
                <div class="alert alert-success" role="alert">
                    Good job! here is your flag: <?= file_get_contents("/flag.txt") ?>
                </div>
            <?php } else { ?>
                <div class="alert alert-danger" role="alert">
                    Incorrect username or password
                </div>
            <?php } ?>
        <?php } ?>
        <div class="card mb-2">
            <h5 class="card-header">Login</h5>
            <div class="card-body">
                <form action="/" method="post">
                    <div class="mb-3 row">
                        <label class="col-sm-2 col-form-label">Username</label>
                        <div class="col-sm-10">
                            <input type="text" class="form-control" name="username">
                        </div>
                    </div>
                    <div class="mb-3 row">
                        <label class="col-sm-2 col-form-label">Password</label>
                        <div class="col-sm-10">
                            <input type="password" class="form-control" name="password">
                        </div>
                    </div>
                    <input class="btn btn-primary" type="submit" value="Submit">
                </form>
            </div>
        </div>
        <a href="/source.php">Source</a>
    </div>

    <style>
        .container {
            max-width: 800px;
        }
    </style>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/js/bootstrap.bundle.min.js" integrity="sha384-JEW9xMcG8R+pH31jmWH6WWP0WintQrMb4s7ZOdauHnUtxwoG2vI5DkLtS3qm9Ekf" crossorigin="anonymous"></script>
</body>

</html>