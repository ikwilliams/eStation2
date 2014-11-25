<?php
	session_start();    //Start SESSION
    $sessionid = session_id();
    $_SESSION['globals']['session_id'] = $sessionid;
	
//    require_once './handyfunctions.php';
      
    $fileXML = "../systemmonitoring.xml";
    $xml = simplexml_load_file($fileXML);
	$_SESSION['globals']['logfile_path'] = (string) $xml->logfile_path;
	$_SESSION['globals']['reportfile_path'] = (string) $xml->reportfile_path;

    $task = '';
    if ( isset($_REQUEST['task'])){
        $task = $_REQUEST['task'];   // Get this from Ext AJAX call
    }
    switch($task){

        case "getLogFileList":

            $filetype = "log";
            if ( isset($_REQUEST['filetype'])){
                $filetype = $_REQUEST['filetype'];   // Get this from Ext AJAX call
            }
            if ($filetype =='log')
                 $dirpath= $_SESSION['globals']['logfile_path'];
            else $dirpath= $_SESSION['globals']['reportfile_path'];

//            if ( isset($_POST['dirpath']) && trim($_POST['dirpath']) != ''){
//                $dirpath = $_POST['dirpath'];   // Get this from Ext AJAX call
//            }

            $history = false;
            if ( isset($_REQUEST['history'])){
//                echo "_POST['history']: " . $_POST['history'] . "\n";
                $history = $_REQUEST['history'];   // Get this from Ext AJAX call
            }	            
            getLogFileList($dirpath, $filetype, $history);
            break;

        case "getLogFile":
            $logfilename= '';
            if ( isset($_REQUEST['logfilename'])){
                $logfilename = $_REQUEST['logfilename'];   // Get this from Ext AJAX call
            }

            $logfilepath= $_SESSION['globals']['logfile_path'];
            if ( isset($_REQUEST['logfilepath']) && trim($_REQUEST['logfilepath']) != ''){
                $logfilepath = $_REQUEST['logfilepath'];   // Get this from Ext AJAX call
            }			
            getLogFile($logfilename, $logfilepath);
            break;

        default:
          echo "{failure:true}";  // Simple 1-dim JSON array to tell Ext the request failed.
          break;
    }



    function display_filesize($filesize){

        if(is_numeric($filesize)){
        $decr = 1024; $step = 0;
        $prefix = array('Byte','KB','MB','GB','TB','PB');

        while(($filesize / $decr) > 0.9){
            $filesize = $filesize / $decr;
            $step++;
        }
        return round($filesize,1).' '.$prefix[$step];
        } else {

        return 'NaN';
        }

    }


    function getLogFileList($dirpath, $filetype, $history)
    {
        if(is_dir($dirpath) ){

            require("dir_functions.php");

            // You need a valid mlsid or some other identifier
//            $propid = $_REQUEST['mlsid']; // I assume the id will be in the querystring

            // This is the full match pattern based upon your selections above
            //$pattern = $propid."_*.".$strExt;
//            echo 'history: '.$history . "\n";
            if ($history == "true") {
                if ($filetype == "log")
                    $pattern = "*.log*";
                else if ($filetype == "report")
                    $pattern = "report_*.txt*";
                else if ($filetype == "derived")
                    $pattern = "*derived_*.log*";
                else if ($filetype == "ingest")
                    $pattern = "ingest_*.log*";
            }
            else {
                if ($filetype == "log")
                    $pattern = "*.log";
                else if ($filetype == "report")
                    $pattern = "report_*.txt";
                else if ($filetype == "derived")
                    $pattern = "*derived_*.log";
                else if ($filetype == "ingest")
                    $pattern = "*ingest_*.log";
            }
//            echo 'pattern: '.$pattern;
            $matches=GetMatchingFiles(GetContents($dirpath),$pattern);
            if (sizeof($matches) > 0) {
                $jsonresult = '[';
                foreach ($matches as $filename) {
                    $file = file_get_contents($dirpath . '/' . $filename, FILE_TEXT);
                    $filestatus = '';
                    if(strpos($file,' FATAL ')!=false)
                        $filestatus = 'red';
                    else if(strpos($file,' ERROR ')!=false)
                        $filestatus = 'red';
                    else if(strpos($file,' CRITICAL ')!=false)
                        $filestatus = 'red';
                    else if(strpos($file,' CLOSED ')!=false)
                        $filestatus = 'brown';
                    else if(strpos($file,' WARNING ')!=false)
                        $filestatus = 'orange';
                    else if(strpos($file,' WARN ')!=false)
                        $filestatus = 'orange';
                    else if(strpos($file,' INFO ')!=false)
                        $filestatus = 'green';
                    else if(strpos($file,' TRACE ')!=false)
                        $filestatus = 'gray';
                    else if(strpos($file,' DEBUG ')!=false)
                        $filestatus = 'gray';

                    $filenameformatted = $filename;
                    if ($filestatus != '')
                       $filenameformatted = "<span style='color:$filestatus;'>$filename</span>";

                    $filepath = "$dirpath/$filename";
                    $filedate = filectime($filepath);
                    $filedate = date("Y-m-d H:i", $filedate);
                    $filesize = filesize($filepath);   // get filesize in byte
                    $filesize = display_filesize($filesize);
                    
                    $jsonresult .= '{"filename":"'. $filename .'","filenameformatted":"'. $filenameformatted .'","filesize":"'. $filesize . '","filedate":"'. $filedate .'","filestatus":"' . $filestatus . '"},';
                }
                $jsonresult = substr($jsonresult, 0, strlen($jsonresult)-1) . "]";
                echo $jsonresult ;

    //			$jsonresult = '[';
    //			foreach (new DirectoryIterator($logfilepath) as $fileInfo) {
    //				if($fileInfo->isDot()) continue;
    //				$jsonresult .= '{"filename":"'.$fileInfo->getFilename() .'","filesize":"'. $fileInfo->getSize() . '","filedate":"'. $fileInfo->getATime() .'","filepath":"' . $fileInfo->getPathname() . '"},';
    //
    //				// echo $fileInfo->getFilename() . " " . $fileInfo->getSize() . " " . $fileInfo->getPathname() . " " . $fileInfo->getATime()  . "\n";
    //			}
    //			$jsonresult = substr($jsonresult, 0, strlen($jsonresult)-1) . "]";
    //			echo $jsonresult ;
            }
            else echo '{"filename":"","filenameformatted":"","filesize":"","filedate":"","filestatus":""}';	// "No files found in folder";

        } else {
            echo '{"filename":"","filenameformatted":"","filesize":"","filedate":"","filestatus":""}';	// "Log file folder doesn't exist";
        }
    }

	function getLogFile($logfilename, $logfilepath)
    {
		 if (is_dir($logfilepath) ) {
			// search for all parts of the log file and merge them
			$file = file_get_contents($logfilepath . '/' . $logfilename, FILE_TEXT);
            $file = str_replace(chr(10), '<br />', $file);
            $file = str_replace(' TRACE ', '<b style="color:gray"> TRACE </b>', $file);
            $file = str_replace(' DEBUG ', '<b style="color:gray"> DEBUG </b>', $file);
	        $file = str_replace(' INFO ', '<b style="color:green"> INFO </b>', $file);
            $file = str_replace(' WARNING ', '<b style="color:orange"> WARN </b>', $file);
            $file = str_replace(' WARN ', '<b style="color:orange"> WARN </b>', $file);
	        $file = str_replace(' ERROR ', '<b style="color:red"> ERROR </b>', $file);
	        $file = str_replace(' CRITICAL ', '<b style="color:red"> FATAL </b>', $file);
            $file = str_replace(' FATAL ', '<b style="color:red"> FATAL </b>', $file);
            $file = str_replace(' CLOSED ', '<b style="color:brown"> CLOSED </b>', $file);

			echo $file;
		}
		else {
			echo "Log file folder doesn't exist";
		}
	}
    
    
?>
