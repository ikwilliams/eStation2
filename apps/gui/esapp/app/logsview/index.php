<?php  

    session_start();    //Start SESSION
    $sessionid = session_id();
    $_SESSION['globals']['session_id'] = $sessionid;


    $host=$_SERVER['HTTP_HOST'];
    include ("../language.php");
?>

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="en">
<head>
	<!-- META DATA SECTION : Title, keywords and description in the document language -->
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8"> 
	<meta name="Reference" content="COMM/SITE_NAME">
	<meta name="Title" content="PS/EMMA e-Station">
	<meta name="Creator" content="Bruno Combal and Jur van 't Klooster">
	<meta name="Language" content="en">
	<meta name="Type" content="Numeric code given in the list of document types">
	<meta name="Classification" content="Numeric code from the alphabetical classification list common to all the institutions">
	<meta name="Keywords" content="one or more of the commission specific keywords + european union, eu">
	<meta name="Description" content="European Commission - The Environment Mapping & Monitoring System (EMMA) helps to write environmental reports based on satellite observation">
	<!-- END OF META DATA SECTION -->

    <title>eStation - Log files</title>

    <link rel="shortcut icon" href="../image/amesd_flavicon.ico">

	<!-- EXTJS necessary includes -->
    <link rel="stylesheet" type="text/css" href="../lib/ext/resources/css/ext-all.css"/>
    <link rel="stylesheet" type="text/css" href="../lib/ext/resources/css/xtheme-gray.css" />
	<script type="text/javascript" src="../lib/ext/adapter/ext/ext-base.js"></script>
	<!-- <script type="text/javascript" src="../lib/ext/ext-all-debug.js"></script>   -->
    <script type="text/javascript" src="../lib/ext/ext-all.js"></script>

    <link href="../lib/css/Ext.ux.grid.RowActions.css" rel="stylesheet" type="text/css" />
    <link href="../lib/css/Ext.ux.grid.CellActions.css" rel="stylesheet" type="text/css" />
    <link href="./style.css" rel="stylesheet" type="text/css">

    <script type="text/javascript" src="../lib/Ext.ux.Toast.js"></script>
    <script type="text/javascript" src="../lib/Ext.ux.grid.CheckColumn.js"></script>
    <script type="text/javascript" src="../lib/Ext.ux.grid.RowActions.js"></script>
    <script type="text/javascript" src="../lib/Ext.ux.grid.CellActions.js"></script>

    
	<script type="text/javascript" src="./js/logmonitor.js"></script>

    
<style type="text/css">
    /*SPAN.highlight { background-color:yellow; }*/
    .highlight { background-color: yellow }

    .settings-icon { background: url('./img/settings1small.png') no-repeat 0 0 !important; }

    .report_magnify-icon { background: url('./img/report_magnify.png') no-repeat 0 0 !important; }
    .folder-open-document-text-icon { background: url('./img/folder-open-document-text.png') no-repeat 0 0 !important; }
    .magnifier-left-icon { background: url('./img/magnifier-left.png') no-repeat 0 0 !important; }
    .script-icon { background: url('./img/script.png') no-repeat 0 0 !important; }
    .eye-icon { background: url('./img/eye.png') no-repeat 0 0 !important; }    
</style>

</head>

<body>
    <div id="title">
        <div id="menu"><?php include ("../menu.php"); ?></div>

        <a href="http://<?php echo $host; ?>/">
            <div class="logo"></div>
        </a>
        <?php if ( file_exists("/var/www/DOC") ) {  ?>
            <div id="doc">
                <a href="http://<?php echo $host; ?>/DOC">
                    <img alt="" src="../image/Documents-icon.png" border=0 width="80" align="right" title="eStation Documentation">
                </a>
            </div>
        <?php } ?>
    </div>

    <br><br>

    <h1>Logs on PS e-Station</h1>

    <br>
    <div id="logsview" align="center" style="margin: 15px;"></div>


</body>
</html>
