
Ext.define("esapp.view.analysis.analysisMain",{
    "extend": "Ext.panel.Panel",
    "controller": "analysis-analysismain",
    "viewModel": {
        "type": "analysis-analysismain"
    },

    xtype  : 'analysis-main',

    requires: [
        'Ext.window.Window'
    ],

    name:'analysismain',

    layout: {
        type: 'fit'
    },
    frame: false,
    border: false,
    bodyPadding: '0 0 0 0',

    initComponent: function () {
        var me = this;

        me.defaults = {
            titleAlign: 'center',
            frame: true,
            border: false,
            bodyPadding: 0
        };
        me.tbar = Ext.create('Ext.toolbar.Toolbar', {
            items: [{
                xtype: 'button',
                name: 'newmapbtn',
                text: 'New map',
                iconCls: 'fa fa-cog', // fa-2x fa-spin 'icon-play', // icomoon fonts
                style: { color: 'gray' },
                // glyph: 'xf0c7@FontAwesome',
                scale: 'small',
                handler: 'newMapView'
            },
            '->',
            {
                xtype: 'button',
                name: 'togglebackgroundlayer',
                text: 'Hide Background layer',
                enableToggle: true,
                // iconCls: 'fa fa-cog', // fa-2x fa-spin 'icon-play', // icomoon fonts
                // style: { color: 'gray' },
                // glyph: 'xf0c7@FontAwesome',
                scale: 'small',
                handler: 'toggleBackgroundlayer'
            }]
        });

        me.html = '<div id="backgroundmap_' + me.id + '"></div>';

        me.commonMapView = new ol.View({
//            projection:"EPSG:4326",
            displayProjection:"EPSG:4326",
            center: ol.proj.transform([21, 4], 'EPSG:4326', 'EPSG:3857'),
            zoom: 3
        });

        me.listeners = {
            afterrender: function () {
                if (window.navigator.onLine){
                    var mousePositionControl = new ol.control.MousePosition({
                      coordinateFormat: ol.coordinate.createStringXY(4),
                      projection: 'EPSG:4326',
                      undefinedHTML: '&nbsp;'
                    });

                    var bingStyles = [
                      'Road'
    //                  'Aerial',
    //                  'AerialWithLabels'
                    ];
                    me.backgroundLayers = [];

                    var i, ii;
                    for (i = 0, ii = bingStyles.length; i < ii; ++i) {
                      me.backgroundLayers.push(new ol.layer.Tile({
                        visible: true,
                        preload: Infinity,
                        projection: 'EPSG:4326',
                        source: new ol.source.BingMaps({
                            // My personal key jurvtk@gmail.com for http://h05-dev-vm19.ies.jrc.it/esapp/ created on www.bingmapsportal.com
                            key: 'Alp8PmGAclkgN_QJQTjgrkPlyRdkFfTnayMuMobAxMha_QF1ikefhdMlUQPdxNS3',
                            imagerySet: bingStyles[i]
                        })
                      }));
                    }

                    var _getRendererFromQueryString = function() {
                      var obj = {}, queryString = location.search.slice(1),
                          re = /([^&=]+)=([^&]*)/g, m;

                      while (m = re.exec(queryString)) {
                        obj[decodeURIComponent(m[1])] = decodeURIComponent(m[2]);
                      }
                      if ('renderers' in obj) {
                        return obj['renderers'].split(',');
                      } else if ('renderer' in obj) {
                        return [obj['renderer']];
                      } else {
                        return undefined;
                      }
                    };

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

                    me.backgroundLayers.push(vectorLayer);

                    var featureTooltip = Ext.create('Ext.tip.ToolTip', {
    //                        target: feature,
    //                        anchor: 'right',
                        trackMouse: true,
                        html: 'Tracking while you move the mouse'
                    });
                    /**
                     * Create an overlay to anchor the popup to the map.
                     */
                    var overlay = new ol.Overlay({
                      element: featureTooltip.getEl()
                    });

                    me.map = new ol.Map({
                        layers: me.backgroundLayers,
                        // renderer: _getRendererFromQueryString(),
                        projection:"EPSG:3857",
                        displayProjection:"EPSG:4326",
                        target: 'backgroundmap_'+ me.id,
                        overlays: [overlay],
                        view: me.commonMapView,
                        controls: ol.control.defaults({
                            zoom: false,
                            attribution:false,
                            attributionOptions: /** @type {olx.control.AttributionOptions} */ ({
                              collapsible: true // false to show always without the icon.
                            })
                        }).extend([mousePositionControl])
                    });

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

    //                    var info = document.getElementById('info');
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
                    }, this);

    //                (me.map.getViewport()).on('mousemove', function(evt) {
    //                    var pixel = me.map.getEventPixel(evt.originalEvent);
    //                    displayFeatureInfo(pixel);
    //                });

                    this.map.on('click', function(evt) {
                        var coordinate = evt.coordinate;
                        overlay.setPosition(coordinate);
                        displayFeatureInfo(evt.pixel);
                    });
                }
            }
            // The resize handle is necessary to set the map!
            ,resize: function () {
                var size = [document.getElementById(this.id + "-body").offsetWidth, document.getElementById(this.id + "-body").offsetHeight];
                this.map.setSize(size);
            }
        };

        me.items = [{
            xtype: 'mapview-window',
            title: '<span class="panel-title-style">MAP 1</span>',
            x:30,
            y:50,
            autoShow : true,
            layers: [
                new ol.layer.Tile({
                    source: new ol.source.MapQuest({layer: 'sat'})
//                    ,projection: 'EPSG:4326'
                })
            ],
            projection: 'EPSG:3857' //'EPSG:3857'
        },{
            xtype: 'mapview-window',
            title: '<span class="panel-title-style">MAP 2</span>',
            x:1000,
            y:50,
            autoShow : true,
            layers: [
                new ol.layer.Tile({
                    source: new ol.source.OSM()
//                    ,projection: 'EPSG:4326'
                })
            ],
            projection: 'EPSG:3857' // 'EPSG:3857'
        }];

        me.callParent();
    }
});
