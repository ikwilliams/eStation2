Ext.define('esapp.view.analysis.mapViewController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.analysis-mapview'

    ,addProductLayer: function(productcode, productversion, mapsetcode, subproductcode, legendid, productname) {
        var me = this;
        var params = {
               productcode:productcode,
               mapsetcode:mapsetcode,
               productversion:productversion,
               subproductcode:subproductcode
        };
        me.getView().productdate = '';

        Ext.Ajax.request({
            method: 'GET',
            url:'analysis/gettimeline',
            params: params,
            loadMask:'Loading data...',
            callback:function(callinfo,responseOK,response ){
                var responseJSON = Ext.util.JSON.decode(response.responseText);
                var dataLength = responseJSON.total,
                    data = [],
                    i = 0,
                    color = '#ff0000';

                for (i; i < dataLength; i += 1) {
                    if (i == dataLength-1) {
                        me.getView().productdate = responseJSON.timeline[i]['date'];
                        console.info('assign proddate: ' + me.getView().productdate);
                    }

                    if (responseJSON.timeline[i]['present'] == "true") {
                        color = '#08a355';
                        data.push({
                            x: responseJSON.timeline[i]['datetime'], // the date
                            y: 1,
                            color: color,
                            date: responseJSON.timeline[i]['date'],
                            events: {
                                click: function () {
                                    me.getView().getController().updateProductLayer(productcode,
                                        productversion,
                                        mapsetcode,
                                        subproductcode,
                                        legendid,
                                        this.date);
                                }
                            }
                        });
                    }
                    else {
                        color ='#ff0000';
                        data.push({
                            x: responseJSON.timeline[i]['datetime'], // the date
                            y: 1,
                            color: color,
                            date: responseJSON.timeline[i]['date']
                        });
                    }
                }
                var mapview_timelinechart_container = me.lookupReference('time-line-chart' + me.getView().id);
                mapview_timelinechart_container.timelinechart.series[0].setData(data, false);
                me.getView().getController().redrawTimeLine();

            },
            success: function ( result, request ) {},
            failure: function ( result, request) {}
        });

        var versiontitle = ''
        if (productversion !== 'undefined'){
            versiontitle = ' - <b class="smalltext">' + productversion + '</b>';
        }
        console.info('proddate: ' + me.getView().productdate);
        var mapwvieTitle = productname + versiontitle + ' - <b class="smalltext">' + me.getView().productdate + '</b>';
        this.getView().setTitle(mapwvieTitle);

        //var mapviewtimeline = this.getView().getDockedItems('toolbar[dock="bottom"]')[0];
        //var searchtimeline = 'container[id="product-time-line_' + this.getView().id + '"]'
        //var mapviewtimeline = this.getView().down(searchtimeline);
        var mapviewtimeline = this.lookupReference('product-time-line_' + this.getView().id);
        mapviewtimeline.setHidden(false);
        mapviewtimeline.expand();

        this.getView().productlayer = new ol.layer.Image({
            source: new ol.source.ImageWMS({
                url: 'analysis/getproductlayer',
                crossOrigin: 'anonymous',
                attributions: [new ol.Attribution({
                    html: '&copy; <a href="https://ec.europa.eu/jrc/">eStation 2 </a>'
                })],
                params: {
                    productcode:productcode,
                    productversion:productversion,
                    subproductcode:subproductcode,
                    mapsetcode:mapsetcode,
                    legendid:legendid,
                    'FORMAT': 'image/png'
                },
                serverType: 'mapserver' /** @type {ol.source.wms.ServerType}  ('mapserver') */
            })
        });
        this.getView().map.removeLayer(this.getView().map.getLayers().a[0])
        this.getView().map.addLayer(this.getView().productlayer)

    }

    ,updateProductLayer: function(productcode, productversion, mapsetcode, subproductcode, legendid, clickeddate) {
        this.getView().productlayer = new ol.layer.Image({
            source: new ol.source.ImageWMS({
                url: 'analysis/getproductlayer',
                crossOrigin: 'anonymous',
                attributions: [new ol.Attribution({
                    html: '&copy; <a href="https://ec.europa.eu/jrc/">eStation 2 </a>'
                })],
                params: {
                    productcode:productcode,
                    productversion:productversion,
                    subproductcode:subproductcode,
                    mapsetcode:mapsetcode,
                    legendid:legendid,
                    date:clickeddate,
                    'FORMAT': 'image/png'
                },
                serverType: 'mapserver' /** @type {ol.source.wms.ServerType}  ('mapserver') */
            })
        });
        this.getView().map.removeLayer(this.getView().map.getLayers().a[0])
        this.getView().map.addLayer(this.getView().productlayer)

    }

    ,redrawTimeLine: function () {
        var mapviewtimeline = this.lookupReference('product-time-line_' + this.getView().id);
        var mapview_timelinechart_container = this.lookupReference('time-line-chart' + this.getView().id);
        var timeline_container_size = mapviewtimeline.getSize();
        mapview_timelinechart_container.timelinechart.container.width = timeline_container_size.width;
        mapview_timelinechart_container.timelinechart.setSize(timeline_container_size.width-15, timeline_container_size.height, false);
        mapview_timelinechart_container.timelinechart.reflow();
        mapview_timelinechart_container.timelinechart.redraw();
    }

    ,toggleLink: function(btn, event) {
        var mapviewwin = btn.up().up();

        if (btn.pressed) {
            mapviewwin.map.setView(mapviewwin.mapView);
            btn.setText('Link');
            btn.setIconCls('link');
        }
        else {
            mapviewwin.map.setView(mapviewwin.up().commonMapView);
            btn.setText('Unlink');
            btn.setIconCls('unlink');
        }
    }

    ,openProductNavigator: function(btn, event) {
        var productNavigatorWin = Ext.getCmp(btn.up().up().getId()+'-productnavigator');
        //var productNavigatorWin = btn.up().up().up('window[id='+btn.up().up().getId()+'-productnavigator]');
        //if (Ext.isObject(productNavigatorWin)) {}
        if (!productNavigatorWin){
            productNavigatorWin = new esapp.view.analysis.ProductNavigator({mapviewid:btn.up().up().getId()});
        }
        productNavigatorWin.show();
        //var productsgridstore = productNavigatorWin.lookupReference('productsGrid').getStore('products');
        //if (productsgridstore.isStore) {
        //    productsgridstore.load({loadMask:true});
        //}
    }

    ,addVectorLayer: function(btn){
        // ToDo: Open a new window from which the user can select an in the eStation2 existing or upload a vector layer.
        // ToDo: Have the user set vector layer setting before adding the layer to the map.
        // For now a predifined GeoJSNON  layer with fixed settings is added.

        var me = this;
        var styleCache = {};
        var vectorLayer = new ol.layer.Vector({
          source: new ol.source.GeoJSON({
            projection: 'EPSG:3857',
            url: 'resources/geojson/countries.geojson'
          }),
          style: function(feature, resolution) {
            var text = resolution < 5000 ? feature.get('name') : '';
            if (!styleCache[text]) {
              styleCache[text] = [new ol.style.Style({
                fill: new ol.style.Fill({
                  color: 'rgba(255, 255, 255, 0.6)'
                }),
                stroke: new ol.style.Stroke({
                  color: '#319FD3',
                  width: 1
                }),
                text: new ol.style.Text({
                  font: '12px Calibri,sans-serif',
                  text: text,
                  fill: new ol.style.Fill({
                    color: '#000'
                  }),
                  stroke: new ol.style.Stroke({
                    color: '#fff',
                    width: 3
                  })
                })
              })];
            }
            return styleCache[text];
          }
        });

        me.layers.push(vectorLayer);


        var featureTooltip = Ext.create('Ext.tip.ToolTip', {
            //target: feature,
            //anchor: 'right',
            trackMouse: true,
            html: 'Tracking while you move the mouse'
        });
        /**
         * Create an overlay to anchor the popup to the map.
         */
        var overlay = new ol.Overlay({
          element: featureTooltip.getEl()
        });

        me.map.overlays.push(overlay);

        var highlightStyleCache = {};

        var featureOverlay = new ol.FeatureOverlay({
          map: me.map,
          style: function(feature, resolution) {
            var text = resolution < 5000 ? feature.get('name') : '';
            if (!highlightStyleCache[text]) {
              highlightStyleCache[text] = [new ol.style.Style({
                stroke: new ol.style.Stroke({
                  color: '#f00',
                  width: 1
                }),
                fill: new ol.style.Fill({
                  color: 'rgba(255,0,0,0.1)'
                }),
                text: new ol.style.Text({
                  font: '12px Calibri,sans-serif',
                  text: text,
                  fill: new ol.style.Fill({
                    color: '#000'
                  }),
                  stroke: new ol.style.Stroke({
                    color: '#f00',
                    width: 3
                  })
                })
              })];
            }
            return highlightStyleCache[text];
          }
        });

        var highlight;
        var displayFeatureInfo = function(pixel) {

            var feature = me.map.forEachFeatureAtPixel(pixel, function(feature, layer) {
                return feature;
            });

            //var info = document.getElementById('info');
            if (feature) {
                featureTooltip.html = feature.getId() + ': ' + feature.get('name');
            } else {
                featureTooltip.html = '&nbsp;';
            }

            if (feature !== highlight) {
                if (highlight) {
                    featureOverlay.removeFeature(highlight);
                }
                if (feature) {
                    featureOverlay.addFeature(feature);
                }
                highlight = feature;
            }
        };

        me.mon(Ext.select('ol-viewport'), 'mousemove', function(evt){
            var pixel = me.map.getEventPixel(evt.originalEvent);
            displayFeatureInfo(pixel);
        }, me);

        //(me.map.getViewport()).on('mousemove', function(evt) {
        //    var pixel = me.map.getEventPixel(evt.originalEvent);
        //    displayFeatureInfo(pixel);
        //});

        me.map.on('click', function(evt) {
            var coordinate = evt.coordinate;
            overlay.setPosition(coordinate);
            displayFeatureInfo(evt.pixel);
        });
    }
});
