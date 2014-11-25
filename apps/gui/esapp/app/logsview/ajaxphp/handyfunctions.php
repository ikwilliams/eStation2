<?php
    function JEncode($arr){
        if (version_compare(PHP_VERSION,"5.2","<"))
        {
            require_once("JSON.php");   //if php<5.2 need JSON class
            $json = new Services_JSON();  //instantiate new json object
            $data=$json->encode($arr);    //encode the data in json format
        } else
        {
            $data = json_encode($arr);    //encode the data in json format
        }
        return $data;
    }

    /*
    * Date format converter
    * Dates have the format YYYYMMDD, where YYYY is the four digits year,
    * MM is the two digit month and DD is the dekad (01, 11 or 21).
    * The dekad are counted from the 1st of January 1980: 1 == 19800101.
    */
    function priv_dekad2vgt($dekadIn){
        $dekad=$dekadIn;
        $year = floor($dekad/36);
        $month = floor(($dekad - 36*$year)/3);
        $day = $dekad - 36*$year - 3*$month;
        $day = 1+10*$day;

        $date = ($year+1980)*10000+($month+1)*100+$day;
        return $date;
    }
//    function vgt2dekad(thisform){
//        var date=thisform.dateIn.value;
//
//        var year = Math.floor(date/10000);
//        var month = Math.floor((date - 10000*year)/100);
//        var day = date - 10000*year - 100*month;
//
//        var dekad = 36*(year-1980) + 3*(month-1) + Math.floor(day/10)+1;
//        thisform.dekaddate.value=dekad;
//    }

    function vgt2dekad($dateIn){      // $dateIn must have the format YYYYMMDD

        $year  = floor($dateIn/10000);
        $month = floor(($dateIn - 10000*$year)/100);
        $day   = $dateIn - 10000*$year - 100*$month;

        $dekad = 36*($year-1980) + 3*($month-1) + floor($day/10)+1;
        return $dekad;
    }

    /*
    *   This function, html2rgb recognizes HTML or CSS colors in format #(hex_red)(hex_green)(hex_blue),
    *   where hex_red, hex_green and hex_blue are 1 or 2-digit hex-representations of red, green or blue color components.
    *   # character in the beginning can be omitted. Function returns array of three integers in range (0..255) or false
    *   when it fails to recognize color format.
    *
    */
    function html2rgb($color)
    {
        if ($color[0] == '#')
            $color = substr($color, 1);

        if (strlen($color) == 6)
            list($r, $g, $b) = array($color[0].$color[1],
                                     $color[2].$color[3],
                                     $color[4].$color[5]);
        elseif (strlen($color) == 3)
            list($r, $g, $b) = array($color[0].$color[0], $color[1].$color[1], $color[2].$color[2]);
        else
            return false;

        $r = hexdec($r); $g = hexdec($g); $b = hexdec($b);

        return array($r, $g, $b);
    }

    /*
    *   Second function, rgb2html converts its arguments (r, g, b) to hexadecimal html-color string #RRGGBB
    *   Arguments are converted to integers and trimmed to 0..255 range. It is possible to call it with array argument
    *   rgb2html($array_of_three_ints) or specifying each component value separetly rgb2html($r, $g, $b).
    */
    function rgb2html($r, $g=-1, $b=-1)
    {
        if (is_array($r) && sizeof($r) == 3)
            list($r, $g, $b) = $r;

        $r = intval($r); $g = intval($g);
        $b = intval($b);

        $r = dechex($r<0?0:($r>255?255:$r));
        $g = dechex($g<0?0:($g>255?255:$g));
        $b = dechex($b<0?0:($b>255?255:$b));

        $color = (strlen($r) < 2?'0':'').$r;
        $color .= (strlen($g) < 2?'0':'').$g;
        $color .= (strlen($b) < 2?'0':'').$b;
        return '#'.$color;
    }
?>
