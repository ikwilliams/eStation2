<?php


    /*
    *   This function, gets the passed label in the passed language.
    */
    function getLabelTranslation($db, $label, $language = 'eng')
    {
//        echo $label;
        if (substr($label,0,3) == 'db_') {     // If grouplabel is translated, get it's translation in the selected language from the database.
            $language = strtolower($language);

            $getLabel_i18n =   " SELECT * "
                              ." FROM ".DBSCHEMA.".i18n "
                              ." WHERE label = '" . $label . "'";

            $res = $db->query($getLabel_i18n);
            while ($row = $res->fetch()) {
                $LabelTranslated = $row[$language];
            }
            if ($LabelTranslated != '') return $LabelTranslated;
            else return $label;
        }
        else return $label;
    }


/*
*   This function generates the legendHTML.
*/

    function generateLegendHTML($db, $legend_id, $language = 'eng')
    {
        $sql =  " SELECT ls.* "
               ." FROM ".DBSCHEMA.".legend_step ls "
               ." WHERE ls.legend_id = " . $legend_id
               ." ORDER BY from_step ";
//        echo $sql;
        $result = $db->query($sql);

        $legendHTML = "";
        $getTotSteps =   " SELECT ts.TotSteps, tsl.TotColorLabels, tgl.TotGroupLabels "
                        ." FROM ( SELECT count(*) as TotSteps FROM ".DBSCHEMA.".legend_step ls1 WHERE ls1.legend_id = " . $legend_id . " ) ts, "
                        ."      ( SELECT count(color_label) as TotColorLabels FROM ".DBSCHEMA.".legend_step ls2 WHERE ls2.legend_id = " . $legend_id . " AND trim(color_label) != '') tsl, "
                        ."      ( SELECT count(group_label) as TotGroupLabels FROM ".DBSCHEMA.".legend_step ls3 WHERE ls3.legend_id = " . $legend_id . " AND trim(group_label) != '') tgl ";
//        echo $getTotSteps;
        $res = $db->query($getTotSteps);
        while ($rowTotSteps = $res->fetch()) {
            $TotSteps = $rowTotSteps['totsteps'];
            $TotColorLabels = $rowTotSteps['totcolorlabels'];
            $TotGroupLabels = $rowTotSteps['totgrouplabels'];
        }

        if ($TotSteps > 20)
            $legendWidth=750;
        else $legendWidth=450;

        if ($TotSteps > 0)
            $stepWidth = $legendWidth/$TotSteps;
        else $stepWidth = $legendWidth;
        
        if ($stepWidth < 3)
            $stepWidth = 1;


        if ($TotColorLabels > 0)
            $ColumnSpan = round($TotSteps/$TotColorLabels);
        else $ColumnSpan = 1;

        $getLegendName = "SELECT legend_name FROM ".DBSCHEMA.".legend WHERE legend_id = " . $legend_id;
        $res = $db->query($getLegendName);
        while ($row = $res->fetch()) {
            $LegendName = $row['legend_name'];
        }

        $legendTableBegin = '<table class="legendMap" style="border: 1px solid white; margin: 0px; padding: 0px; "> ';
        $legendHeader = '<tr><td colspan="'.$TotSteps.'"><br /><h2>Legend: '.getLabelTranslation($db, $LegendName, $language).'</h2><br /></td></tr>';

        $legendGroupLabels = '';
        if ($TotGroupLabels > 0) {
            $legendGroupLabels = '<tr>';
            $PrevGroupLabel = '';
            $Counter = 0;
            while ($row = $result->fetch()) {
                $GroupLabel = getLabelTranslation($db, $row['group_label'], $language).'&nbsp;';

                if (trim($GroupLabel) == $PrevGroupLabel) {
                    $Counter += 1;
                    $PrevGroupLabel = $GroupLabel;
                }
                else {
//                    $legendColors = $legendColors . '<td><img src="img/clearpixel.gif" width="1" height="15" /></td>';
                    if ($Counter != 0) {
                         $legendGroupLabels = $legendGroupLabels . '<td colspan="'.$Counter.'" align="center">'.$PrevGroupLabel.'</td><td rowspan="3" style="background-color: black;"><img src="img/clearpixel.gif" width="1" height="15" /></td>';
                    }
                    $PrevGroupLabel = $GroupLabel;
                    $Counter = 1;
               }
            }
//            $legendGroupLabels = $legendGroupLabels . '<td rowspan="3" style="background-color: black;"><img src="img/clearpixel.gif" width="1" height="15" /></td>';
            $legendGroupLabels = $legendGroupLabels . '<td colspan="'.$Counter.'" align="center">'.$PrevGroupLabel.'</td>';
//            $legendGroupLabels = $legendGroupLabels . '<td rowspan="3" style="background-color: black;"><img src="img/clearpixel.gif" width="1" height="15" /></td>';
            $legendGroupLabels = $legendGroupLabels . '</tr>';
//       echo $legendGroupLabels;
       }

        $legendColors = '<tr>';
        while ($row = $result->fetch()) {
            // convert $row['color_rgb'] from RGB to html color
            $color_rgb = explode(" ", $row['color_rgb']);
            $color_html = rgb2html($color_rgb);
            if ($TotSteps <= 1)
                $legendColors = $legendColors . '<td><img src="img/clearpixel.gif" width="5" height="15" /></td>';   // Add 5px space between colors.

            $legendColors = $legendColors . '<td style="background-color: '.$color_html.';"><img src="img/clearpixel.gif" width="'.$stepWidth.'" height="15" /></td>';
        }
        $legendColors = $legendColors . '</tr>';


        $legendColorLabels = '<tr>';
        while ($row = $result->fetch()) {
            if (trim($row['color_label']) != '')
                $ColorLabel = '&nbsp;'.getLabelTranslation($db, $row['color_label'], $language).'&nbsp;';
            else $ColorLabel = '<img src="img/clearpixel.gif" width="'.$stepWidth.'" height="15" />';   // No label exists so fill space transparent image
            // maybe here a function has to analize the color label on its length and put <BR /> where needed!

            if ($TotSteps <= 1) {
//                $legendColorLabels = $legendColorLabels . '<td><img src="img/clearpixel.gif" width="5" height="15" /></td>';   
                $legendColorLabels = $legendColorLabels . '<td align="center">'.$ColorLabel.'</td>';
            }
            else {
//                if (trim($row['color_label']) != '')
                    $legendColorLabels = $legendColorLabels . '<td align="center">'.$ColorLabel.'</td>';     // colspan="'.$ColumnSpan.'"
            }
        }
        $legendColorLabels = $legendColorLabels . '</tr>';
        $legendTableEnd = '</table>';

        $legendHTML =  $legendTableBegin . $legendHeader . $legendGroupLabels . $legendColors  . $legendColorLabels . $legendTableEnd;
        return $legendHTML;
    }

?> 
