
from config import es_constants
import mapscript

MapserverVersion = mapscript.msGetVersion()
#print MapserverVersion


def getmap():
    productfile = '/data/processing/vgt_ndvi/WGS84_Africa_1km/tif/ndv/20130701_vgt_ndvi_ndv_WGS84_Africa_1km.tif'

    #####   create MAP OBJECT   #####

    # create a new mapfile from scratch
    productmap = mapscript.mapObj(es_constants.template_mapfile)
    #productmap.save('temp.map')
    productmap.setSize(736, 782)
    productmap.setExtent(-4863270.2540311385, -7205400.673576976, 9538688.86734863, 8096680.892889029)
    productmap.units = mapscript.MS_DD
    #productmap.imagecolor.setRGB(255, 255, 255)

    # create a layer for the raster
    layer = mapscript.layerObj(productmap)
    layer.name = 'testlayer'
    layer.type = mapscript.MS_RASTER
    layer.status = mapscript.MS_ON
    layer.data = productfile
    return productmap


#
#//  ############    extent    #############
#    $extent = explode(" ", $_SESSION['current_status']['extent']);
#//  $extent = $current_status['extent'];
#    $map->setextent($extent[0], $extent[1], $extent[2], $extent[3]);
#
#//	##############  size   #################
#	$map->setSize($_SESSION['current_status']['map_width'],$_SESSION['current_status']['map_height']);
#
#
#//	############    projection    #############
#	$map->setProjection($_SESSION['globals']['projection_map']);
#
#//	############    WEB   ############
#	/*	$web_obj = $map->web;
#		$web_obj->set("imagepath", 'mapserver/temp/');
#	*/
#
#//	############    OUTPUT FORMAT   ############
#	$output_format = $map->outputformat;
#	$output_format->set("driver", "GD/PNG");
#	$output_format->setOption("INTERLACE", "OFF");

#if (file_exists($_SESSION['current_variable']['complete_filepath']) ){
#    foreach ($_SESSION['current_variable']['irregular_ranges'] as $s){ // $s = ['range_1'] see getVariableInfo.php
#        //print_r($s);
#        $processing_scale = 'SCALE='.$s['bounds'];  // min(legend_step.from_step) max(legend_step.to_step) example: 'SCALE=-7000,10000'
#
#        $_SESSION['globals']['minbuckets']=256;
#        $_SESSION['globals']['maxbuckets']=10000;
#        //   $num_buckets = count($s)-1; // or  $s['totsteps']
#        if ($s['minstepwidth']>0){
#            $num_buckets = round($s['totwidth'] / $s['minstepwidth'], 0);
#        } else {
#            $num_buckets = $_SESSION['globals']['maxbuckets'];
#        }
#
#        if ($num_buckets < $_SESSION['globals']['minbuckets']){
#            $num_buckets = $_SESSION['globals']['minbuckets'];
#        } else if ($num_buckets>$_SESSION['globals']['maxbuckets']){
#            $num_buckets = 0;
#        }
#        if ($num_buckets>0){
#            $processing_buckets = 'SCALE_BUCKETS='.$num_buckets;
#        }
#        //   $processing_buckets = 'SCALE_BUCKETS=10000';
#
#        $processing_novalue = ''; // NODATA=255
#        if ( isset($_SESSION['current_variable']['nodata']) &&  !is_null($_SESSION['current_variable']['nodata']) ) {
#            for($class=0;$class<=$s['totsteps']-1;$class++){ // (count($s)-2)
#                $min_step = $s['step_'.$class]['from'];
#                $max_step = $s['step_'.$class]['to'];
#                if ($_SESSION['current_variable']['nodata']>=$min_step && $_SESSION['current_variable']['nodata']<$max_step){
#                    $setNoData = false;
#                    break;
#                }
#                else {
#                    $setNoData = true;
#                }
#            }
#            if ($setNoData)
#                $processing_novalue = 'NODATA='.$_SESSION['current_variable']['nodata'];
#        }
#
#        $layer_name = $_SESSION['current_variable']['short_name'];
#
#        // add main layer to map
#        $variable_layer = ms_newLayerObj($map);
#        $variable_layer->set("name", $layer_name);
#        $variable_layer->set("data", $_SESSION['current_variable']['complete_filepath']);
#        $variable_layer->set("status", MS_ON);
#        $variable_layer->set("type", MS_LAYER_RASTER);
#        $variable_layer->setProjection($_SESSION['current_variable']['projection']);
#
#        // scale & buckets
#        if ($num_buckets>0){
#            $variable_layer->setProcessing($processing_scale);
#            $variable_layer->setProcessing($processing_buckets);
#        }
#        if ($processing_novalue!=''){
#            $variable_layer->setProcessing($processing_novalue);
#        }
#
#        for($ss=0;$ss<=$s['totsteps']-1;$ss++){ // (count($s)-2)
#            $min_step = $s['step_'.$ss]['from'];
#            $max_step = $s['step_'.$ss]['to'];
#            $color = explode(" ",$s['step_'.$ss]['color']);
#            $expression_string = '([pixel] >= '.$min_step.' and [pixel] < '.$max_step.')';
#
#            // defines class object and style
#            $class = ms_newClassObj($variable_layer);
#            $class->set('name',$layer_name.'_'.$ss);
#            $class->setExpression($expression_string);
#            $style = ms_newStyleObj($class);
#            $style->color->setRGB($color[0], $color[1], $color[2]);
#
#        }
#    }
#}
#else {
#    $_SESSION['current_status']['error_layers'] = $_SESSION['current_status']['error_layers'] . "Image layer file missing for ".$_SESSION['current_variable']['short_name']."!<BR />";
#}

