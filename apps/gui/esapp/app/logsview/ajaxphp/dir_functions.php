<?php
    function GetMatchingFiles($files, $search) {

       // Split to name and filetype
       if(strpos($search,".")) {
        $baseexp=substr($search,0,strpos($search,"."));
        $typeexp=substr($search,strpos($search,".")+1,strlen($search));
      } else {
         $baseexp=$search;
        $typeexp="";
       }

       // Escape all regexp Characters
       $baseexp=preg_quote($baseexp);
      $typeexp=preg_quote($typeexp);

       // Allow ? and *
      $baseexp=str_replace(array("\*","\?"), array(".*","."), $baseexp);
      $typeexp=str_replace(array("\*","\?"), array(".*","."), $typeexp);

       // Search for Matches
       $i=0;
       foreach($files as $file) {
        $filename=basename($file);

        if(strpos($filename,".")) {
          $base=substr($filename,0,strpos($filename,"."));
          $type=substr($filename,strpos($filename,".")+1,strlen($filename));
        } else {
           $base=$filename;
          $type="";
         }

        if(preg_match("/^".$baseexp."$/i",$base) && preg_match("/^".$typeexp."$/i",$type))  {
          $matches[$i]=$file;
           $i++;
         }
       }
       return $matches;
    }


    // Returns all Files contained in given dir, including subdirs if $subdir = true
    function GetContents($dir,$files=array(),$subdir=false) {
     if(!($res=opendir($dir))) exit("$dir doesn't exist!");
      while(($file=readdir($res))==TRUE)
       if($file!="." && $file!="..")
        if(is_dir("$dir/$file")) {
          if ($subdir)
             $files=GetContents("$dir/$file",$files);
        }
        else array_push($files,"$file");

     closedir($res);
     return $files;
    }





    //    files can be sorted on name and stat() attributes, ascending and descending:
    //
    //    name    file name
    //    dev     device number
    //    ino     inode number
    //    mode    inode protection mode
    //    nlink   number of links
    //    uid     userid of owner
    //    gid     groupid of owner
    //    rdev    device type, if inode device *
    //    size    size in bytes
    //    atime   time of last access (Unix timestamp)
    //    mtime   time of last modification (Unix timestamp)
    //    ctime   time of last inode change (Unix timestamp)
    //    blksize blocksize of filesystem IO *
    //    blocks  number of blocks allocated
    //
    //    Example:
    //    $r = myscandir('./book/', '/^article[0-9]{4}\.txt$/i', 'ctime', 1);
    //    print_r($r);
    function myscandir($dir, $exp, $how='name', $desc=0)
    {
        $r = array();
        $dh = @opendir($dir);
        if ($dh) {
            while (($fname = readdir($dh)) !== false) {
                if (preg_match($exp, $fname)) {
                    $stat = stat("$dir/$fname");
                    $r[$fname] = ($how == 'name')? $fname: $stat[$how];
                }
            }
            closedir($dh);
            if ($desc) {
                arsort($r);
            }
            else {
                asort($r);
            }
        }
        return(array_keys($r));
    }


//		$filter = '*.log*';
//        $r = sdir($logfilepath, $filter);
//        print_r($r);
    function sdir( $path='.', $mask='*', $nocache=0 ){
        static $dir = array(); // cache result in memory
        if ( !isset($dir[$path]) || $nocache) {
            $dir[$path] = scandir($path);
        }
        foreach ($dir[$path] as $i=>$entry) {
            if ($entry!='.' && $entry!='..' && fnmatch($mask, $entry) ) {
                $sdir[] = $entry;
            }
        }
        return ($sdir);
    }




    function my_handler($filename) {
      echo $filename . "\n";
    }
// find_files('c:/', '/php$/', 'my_handler');
    
    function find_files($path, $pattern, $callback) {
      $path = rtrim(str_replace("\\", "/", $path), '/') . '/';
      $matches = Array();
      $entries = Array();
      $dir = dir($path);
      while (false !== ($entry = $dir->read())) {
        $entries[] = $entry;
      }
      $dir->close();
      foreach ($entries as $entry) {
        $fullname = $path . $entry;
        if ($entry != '.' && $entry != '..' && is_dir($fullname)) {
          find_files($fullname, $pattern, $callback);
        } else if (is_file($fullname) && preg_match($pattern, $entry)) {
          call_user_func($callback, $fullname);
        }
      }
    }

?>

