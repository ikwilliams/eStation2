Ext.define('esapp.view.analysis.analysisMainController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.analysis-analysismain'

    ,newMapView: function() {

        var newMapViewWin = new esapp.view.analysis.mapView({
            epsg: 'EPSG:4326'
        });
        this.getView().add(newMapViewWin);
        newMapViewWin.show();
    }

    ,toggleBackgroundlayer: function(btn, event) {
        var analysismain = btn.up().up();
        var i, ii;
        if (btn.pressed){
            btn.setText('Show Background layer');
            analysismain.map.removeControl(analysismain.mousePositionControl);
            for (i = 0, ii = analysismain.backgroundLayers.length; i < ii; ++i) {
                analysismain.backgroundLayers[i].setVisible(!btn.pressed);
            }
        }
        else {
            btn.setText('Hide Background layer');
            analysismain.map.addControl(analysismain.mousePositionControl);
            for (i = 0, ii = analysismain.backgroundLayers.length; i < ii; ++i) {
                analysismain.backgroundLayers[i].setVisible(analysismain.bingStyles[i] == 'Road');
            }
        }
    }

    ,loadTimeseriesProductsGrid: function() {

        var prodgrid = this.getView().lookupReference('TimeSeriesProductsGrid');
        var myLoadMask = new Ext.LoadMask({
            msg    : 'Loading...',
            target : prodgrid
        });
        myLoadMask.show();

        this.getStore('products').load({
            callback:function(){
                myLoadMask.hide();
            }
        });
    },

    TimeseriesProductsGridRowClick: function(gridview, record){
        var selectedTimeSeriesProducts = gridview.getSelectionModel().selected.items;
        var timeseriesmapsetdatasets = [];
        selectedTimeSeriesProducts.forEach(function(product) {
            // ToDO: First loop the mapsets to get the by the user selected mapset if the product has > 1 mapsets.
            var datasets = product.get('productmapsets')[0].timeseriesmapsetdatasets;
            datasets.forEach(function(datasetObj) {
                timeseriesmapsetdatasets.push(datasetObj);
            });
            //console.info(product.get('productmapsets')[0].timeseriesmapsetdatasets);
        });
        //var productmapset = record.get('productmapsets')[0];

        this.getStore('timeseriesmapsetdatasets').setData(timeseriesmapsetdatasets);

    },

    getTimeseries: function(btn){
        // productcode
        // version
        // mapset
        // [array of subproductcodes of the selected timeseries]
        // WKT

        var timeseriesgrid = this.getView().lookupReference('timeseries-mapset-dataset-grid');
        var selectedTimeSeries = timeseriesgrid.getSelectionModel().selected.items;
        var wkt_polygon = this.getView().lookupReference('wkt_polygon');

        if (selectedTimeSeries.length >0){
            if (Ext.getCmp('radio-year').getValue()){
                if (Ext.getCmp("YearTimeseries").getValue()=='') {
                    Ext.getCmp("YearTimeseries").validate();
                    Ext.Msg.show({
                       title: 'Mandatory field',
                       msg: 'Please select a year!',
                       width: 300,
                       buttons: Ext.MessageBox.OK,
                       animEl: '',
                       icon: Ext.MessageBox.WARNING
                    });
                    return;
                }
            }

            var timeseriesselected = [];
            selectedTimeSeries.forEach(function(product) {
                var productObj = {
                    "productcode": product.get('productcode'),
                    "version": product.get('version'),
                    "subproductcode": product.get('subproductcode'),
                    "mapsetcode": product.get('mapsetcode')
                };

                timeseriesselected.push(productObj);
            });
            console.info(timeseriesselected);
            timeseriesselected = Ext.util.JSON.encode(timeseriesselected);
        }

        Ext.Ajax.request({
           url:"analysis/gettimeseries",
           params:{
               selectedTimeseries: timeseriesselected,
               yearTS: Ext.getCmp("YearTimeseries").getValue(),
               WKT:wkt_polygon.getValue()
           },
           method: 'POST',
           success: function ( result, request ) {
               var json = Ext.util.JSON.decode(result.responseText);
               //var subtitle =  Ext.ux.util.Encoder.htmlDecode(json.countryName) + ' - ' + Ext.ux.util.Encoder.htmlDecode(json.areaName) + ' ( ID: '+json.rasterpointID+')';

           },
           failure: function ( result, request) {

           }
        });

        var newTSChartWin = new esapp.view.analysis.timeseriesChartView({
            wtk: wkt_polygon
        });
        this.getView().add(newTSChartWin);
        newTSChartWin.show();
    }

});
