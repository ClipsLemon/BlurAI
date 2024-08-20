<?php
$ImageMaxSize=min(intval(str_replace('M','000',ini_get('upload_max_filesize'))), intval(str_replace('M','000',ini_get('post_max_size'))));  // в Kb
?>
