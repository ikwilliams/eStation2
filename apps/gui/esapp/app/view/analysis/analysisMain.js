
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
            center: ol.proj.transform([21, 4], 'EPSG:4326', 'EPSG:3857'),
            zoom: 3
        });

        me.listeners = {
            afterrender: function () {
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
                this.backgroundLayers = [];
                var i, ii;
                for (i = 0, ii = bingStyles.length; i < ii; ++i) {
                  this.backgroundLayers.push(new ol.layer.Tile({
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

                this.map = new ol.Map({
                    layers: this.backgroundLayers,
                    // renderer: _getRendererFromQueryString(),
                    target: 'backgroundmap_'+ this.id,
                    view: me.commonMapView,
                    controls: ol.control.defaults({
                        zoom: false,
                        attribution:false,
                        attributionOptions: /** @type {olx.control.AttributionOptions} */ ({
                          collapsible: true // false to show always without the icon.
                        })
                    }).extend([mousePositionControl])
                });

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
                    source: new ol.source.MapQuest({layer: 'sat'}),
                    projection: 'EPSG:4326'
                })
            ],
            epsg: 'EPSG:3857'
        },{
            xtype: 'mapview-window',
            title: '<span class="panel-title-style">MAP 2</span>',
            x:1000,
            y:50,
            autoShow : true,
            layers: [
                new ol.layer.Tile({
                    source: new ol.source.OSM(),
                    projection: 'EPSG:4326'
                })
            ],
            epsg: 'EPSG:3857'

//            xtype: 'window',
//            title: '<span class="panel-title-style">MAP 2</span>',
//            name:'mapwindow2',
//            constrain:true,
//            x:1000,
//            y:50,
//            margin: '0 0 0 0',
//            layout: {
//                type: 'fit'
//            },
//            width:400,
//            height:500,
//            autoShow : true,
//            glyph : 'xf080@FontAwesome',
//            html:'<div id="mymap2"></div>'
//            ,listeners: {
//                afterrender: function () {
//                    this.map = new ol.Map({
//                        target: 'mymap2',
//                        layers: [
//                            new ol.layer.Tile({
//                                source: new ol.source.OSM()
//                            })
//                        ],
//                        view: me.mapview
//                    });
////                    var mainMapWindow = Ext.ComponentQuery.query('window[name=mapwindow1]');
////                    console.info(mainMapWindow);
////                    this.map.bindTo('layergroup', mainMapWindow);
////                    this.map.bindTo('view', mainMapWindow);
//                }
//                // The resize handle is necessary to set the map!
//                ,resize: function () {
//                    var size = [document.getElementById(this.id + "-body").offsetWidth, document.getElementById(this.id + "-body").offsetHeight];
//                    // console.log(size);
//                    this.map.setSize(size);
//                }
//            }
        }];

        me.callParent();
    }
});
