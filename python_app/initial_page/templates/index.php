<!DOCTYPE html>

<html lang="ja" dir="ltr">
    <head>
      <meta charset="utf-8">
      <title></title>
    </head>

<body>
<?php
$script = '<script>
  document.write(window.localStorage.getItem("Customer"));
</script>'; 
?>

<?php
$myfile = fopen("./data.json", "a")  //fileを上書きモードで開く
?>

<?php fwrite($myfile, $script. "\n"); ?>

<?php
fclose($myfile);
?>
<?php header("location: {% url 'initial_page:usual_page' %} ");
?>
</body>
</html>