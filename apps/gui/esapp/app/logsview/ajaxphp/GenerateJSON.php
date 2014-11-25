<?php
		
	// Include the PostgreSQL class
	require_once '../../database/PostgreSQL.php';
    // Connect to PostgreSQL    
    $db = new PostgreSQL();

    require_once '../../common/handyfunctions.php';
//    require_once './generateLegendHTML.php';
      
// mb_language('uni');
// mb_internal_encoding('UTF-8');
	  
//    function JEncode($arr){
//        if (version_compare(PHP_VERSION,"5.2","<"))
//        {
//            // echo $arr;
//            require_once("./JSON.php");   //if php<5.2 need JSON class
//            $json = new Services_JSON();  //instantiate new json object
//            $data=$json->encode($arr);    //encode the data in json format
//        } else
//        {
//            $data = json_encode($arr);    //encode the data in json format
//        }
//        return $data;
//    }

    if ( isset($_POST['SelectedVariableGroup'])){
      $SelectedVariableGroup = $_POST['SelectedVariableGroup'];   // Get this from Ext AJAX call
    }
    else $SelectedVariableGroup = '';


    $task = '';
    if ( isset($_POST['task'])){
        $task = $_POST['task'];   // Get this from Ext AJAX call 
    }
    switch($task){

        case "getLegendSteps":
            $legendid = '';
            if ( isset($_POST['legendid'])){
                $legendid = $_POST['legendid'];   // Get this from Ext AJAX call
            }
            getLegendSteps($db, $legendid);
            break;

        case "getLegendProductList":
            $legendid = '';
            if ( isset($_POST['legendid'])){
                $legendid = $_POST['legendid'];   // Get this from Ext AJAX call
            }
            getLegendProductList($db, $legendid);
            break;

        case "getLegendProperties":
            $legendid = '';
            if ( isset($_POST['legendid'])){
                $legendid = $_POST['legendid'];   // Get this from Ext AJAX call
            }
            getLegendProperties($db, $legendid);
            break;

        case "getLegendColorSchemes":
            getLegendColorSchemes($db);
            break;

        case "checkIfLoggedin":
            checkIfLoggedin();
            break;

        default:
          echo "{failure:true}";  // Simple 1-dim JSON array to tell Ext the request failed.
          break;
    }


    function getLegendSteps($db, $legendid)
    {

        $qLegendSteps =  " SELECT legend_id,  from_step,  to_step,  color_rgb,  color_label,  group_label "
                       . " FROM ".DBSCHEMA.".legend_step "
                       . " WHERE legend_id = $legendid "
                       . " ORDER BY from_step ";
//        echo $qLegendSteps;
        $LegendSteps = $db->query($qLegendSteps);
        $numLegendSteps = $LegendSteps->size();
//                echo "numGroupVariables:" . $numGroupVariables . "   ";

        if(!$LegendSteps || ($numLegendSteps < 0)){ echo "ERROR!"; } // Error, return nothing !
        if($numLegendSteps == 0){ echo "NO LEGEND PROPERTIES FETCHED!"; }

        if($numLegendSteps>0){
            for($i=0; $i<$numLegendSteps; $i++){
                $LegendStepsRecord = $LegendSteps->fetch();
                $arr[] = $LegendStepsRecord;
            }

            $jsonresult = JEncode($arr);

            $cb = isset($_GET['callback']) ? $_GET['callback'] : '';
            echo $cb . '{"total":"'.$numLegendSteps.'","results":'.$jsonresult.'}';

        } else {
            echo '{"total":"0","results":""}';
        }
    }


    function getLegendProductList($db, $legendid)
    {


        $qLegendProductList =  " SELECT prod_descr_name as \"productgroup\", sub_prod_descr_name as \"productname\", default_legend, CASE WHEN default_legend THEN 'icon-ok' ELSE '' END as \"action1\" "
                             . " FROM ".DBSCHEMA.".product_legend "
                             . " WHERE legend_id = $legendid ";
//        echo $qLegendProductList;
        $LegendProductList = $db->query($qLegendProductList);
        $numLegendProductList = $LegendProductList->size();
//                echo "numGroupVariables:" . $numGroupVariables . "   ";

        if(!$LegendProductList || ($numLegendProductList < 0)){ echo "ERROR!"; } // Error, return nothing !
        if($numLegendProductList == 0){ echo "NO LEGEND PROPERTIES FETCHED!"; }

        if($numLegendProductList>0){
            for($i=0; $i<$numLegendProductList; $i++){
                $LegendProductListRecord = $LegendProductList->fetch();
                $arr[] = $LegendProductListRecord;
            }

            $jsonresult = JEncode($arr);

            $cb = isset($_GET['callback']) ? $_GET['callback'] : '';
            echo $cb . '{"total":"'.$numLegendProductList.'","results":'.$jsonresult.'}';

        } else {
            echo '{"total":"0","results":""}';
        }
    }

    function getLegendProperties($db, $legendid)
    {


        $qLegendProperties =  " SELECT legend_id, legend_name, step_type, min_value, max_value, min_real_value, max_real_value, colorbar, step, step_range_from, step_range_to, unit "
                            . " FROM ".DBSCHEMA.".legend "
                            . " WHERE legend_id = $legendid ";

//        echo $qLegendProperties;
        $LegendProperties = $db->query($qLegendProperties);
        $numLegendProperties = $LegendProperties->size();
//                echo "numGroupVariables:" . $numGroupVariables . "   ";

        if(!$LegendProperties || ($numLegendProperties < 0)){ echo "ERROR!"; } // Error, return nothing !
        if($numLegendProperties == 0){ echo "NO LEGEND PROPERTIES FETCHED!"; }

        if($numLegendProperties>0){
            for($i=0; $i<$numLegendProperties; $i++){
                $LegendPropertiesRecord = $LegendProperties->fetch();
//                $GroupVariablesArray["variables"] = $GroupVariablesRecord;
//                $arr[] = $LegendPropertiesRecord; // Don't pass as an array because the result goes into a form which auto store and load doesn't accept an array;
            }

            $jsonresult = JEncode($LegendPropertiesRecord);

            $cb = isset($_GET['callback']) ? $_GET['callback'] : '';

            echo $cb . '{"success":"true","data":'.$jsonresult.'}';

        } else {
            echo '{"success":"false","data":""}';
        }
    }
    
    function getLegendColorSchemes($db)
    {

        $Query = " SELECT l.legend_id, l.legend_name, i.eng "
               . " FROM ".DBSCHEMA.".legend l "
               . "      left outer join ".DBSCHEMA.".i18n i on l.legend_name = i.label"
               . " ORDER BY legend_name ";
//               . " WHERE prod_descr_name = '" . $SelectedVariableGroup . "'"
//               . "   AND sub_prod_descr_name = '" . $SelectedVariable . "'";

//        echo $Query;
        $Results = $db->query($Query);

        $num_rows = $Results->size();
        //     echo 'Nrvars: ' . $num_rows;
        if(!$Results || ($num_rows < 0)){ echo "ERROR!"; } // Error, return nothing !
        if($num_rows == 0){ echo "NO DYNAMIC DATA_MIN FETCHED!"; }

        if($num_rows>0){
            $jsonresult = "[";
            for($i=0; $i<$num_rows; $i++){
                $Rec = $Results->fetch();

                $legend_id = $Rec['legend_id'];
                $legendLabel = $Rec['legend_name'];
                $legendNameENG = $Rec['eng'];
                $legendName = $legendNameENG;
                if ( $legendNameENG == '')
                    $legendName = $legendLabel;

                $sql = "SELECT ls.* FROM ".DBSCHEMA.".legend_step ls WHERE ls.legend_id = " . $legend_id . "ORDER BY from_step";
//              echo $sql;
                $resultLegendSteps = $db->query($sql);

//                $legendHTML = generateLegendHTML($db, $legend_id, 'eng');
//                $legendHTML = str_replace('"', "'", $legendHTML);

                $colorschemeHTML = '<table cellspacing=0 cellpadding=0 width=100%><tr>';
                while ($row = $resultLegendSteps->fetch()) {
                    // convert $row['color_rgb'] from RGB to html color
                    $color_rgb = explode(" ", $row['color_rgb']);
                    $color_html = rgb2html($color_rgb);

                    $colorschemeHTML = $colorschemeHTML . "<td width=".$stepWidth." height=10 style='padding:0; margin:0; background-color: ".$color_html.";'>&nbsp</td>";
                }
                 $colorschemeHTML = $colorschemeHTML . '</tr></table>';

                $jsonresult = $jsonresult . '{"0":"'.$legend_id.'","legend_id":"'.$legend_id.'", "1":"'.$legendName.'","legendname":"'.$legendName.'", "2":"'.$colorschemeHTML.'","colorscheme":"'.$colorschemeHTML.'"},';
            }
            $jsonresult = substr($jsonresult, 0, strlen($jsonresult)-1) . "]";
//           $jsonresult = JEncode($arr);

            $cb = isset($_GET['callback']) ? $_GET['callback'] : '';

            echo $cb . '{"total":"'.$num_rows.'","results":'.$jsonresult.'}';

        } else {
            echo '{"total":"0", "results":""}';
        }
    }

    function checkIfLoggedin()
    {
		// get Login session
	    include('../../loginsystem/include/session.php');
	        
		// global $session;
		// echo 'logedin: '.$_SESSION['session']->logged_in;
 /*
       session_start();                 //Start SESSION
        
        if (isset($_SESSION['globals']['sessionid'])) {
            session_id(strip_tags($_SESSION['globals']['sessionid']));    // get SESSION ID
        }
//        if (isset($GLOBALS['sessionid'])) {
//            session_id(strip_tags($GLOBALS['sessionid']));    // get SESSION ID
//        }        
        if (isset($_COOKIE["PHPSESSID"])) {
            session_id(strip_tags($_COOKIE['PHPSESSID']));    // get SESSION ID
        }
        if (isset($_REQUEST["sessionid"])) {
            session_id(strip_tags($_REQUEST['sessionid']));    // get SESSION ID
        }
*/

        
//        echo "SESSION['logged_in'] : " . $_SESSION['logged_in'];
//        if (isset($_SESSION['logged_in'])) { echo "SESSION[logged_in]: " . $_SESSION['logged_in']; }
//        echo '{"login":"true","user":"'. $session->username .'"}';
        if($_SESSION['session']->logged_in){
//         echo 'true';
         echo '{"login":"true","user":"'. $_SESSION['session']->username .'"}';
//         return true;
        }
        else {
//         echo 'false';
         echo '{"login":"false","user":"'. $_SESSION['session']->username .'"}';
//         return false;
        }
    }
    
?>
