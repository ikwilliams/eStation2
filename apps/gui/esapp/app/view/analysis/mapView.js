
Ext.define("esapp.view.analysis.mapView",{
    "extend": "Ext.window.Window",
    "controller": "analysis-mapview",
    "viewModel": {
        "type": "analysis-mapview"
    },
    xtype: 'mapview-window',

    requires: [
        'Ext.window.Window',
        'Ext.toolbar.Toolbar',
        'Ext.slider.Single'
    ],

    title: '<span class="panel-title-style">MAP title</span>',
    margin: '0 0 0 0',
    layout: {
        type: 'fit'
    },
    width:500,
    height:600,
    minWidth:400,
    minHeight:400,
    // glyph : 'xf080@FontAwesome',
    constrain: true,
    autoShow : false,
    closeable: true,
    maximizable: true,
    collapsible: true,
    frame: false,
    border: false,

    layers: [],
    epsg: 'EPSG:4326',

    tools: [
    {
        type: 'gear',
        tooltip: 'Map tools menu',
        callback: function (mapwin) {
            // toggle hide/show toolbar and adjust map size.
            var sizeWinBody = [];
            var mapToolbar = mapwin.getDockedItems('toolbar[dock="top"]')[0];
            var widthToolbar = mapToolbar.getWidth();
            var heightToolbar = mapToolbar.getHeight();
            if (mapToolbar.hidden == false) {
                mapToolbar.setHidden(true);
                sizeWinBody = [document.getElementById(mapwin.id + "-body").offsetWidth, document.getElementById(mapwin.id + "-body").offsetHeight+heightToolbar];
            }
            else {
                mapToolbar.setHidden(false);
                sizeWinBody = [document.getElementById(mapwin.id + "-body").offsetWidth, document.getElementById(mapwin.id + "-body").offsetHeight-heightToolbar];
            }
            mapwin.map.setSize(sizeWinBody);
        }
    }],

    initComponent: function () {
        var me = this;

        me.tbar = Ext.create('Ext.toolbar.Toolbar', {
            dock: 'top',
            autoShow: true,
            alwaysOnTop: true,
            hidden: false,
            border: false,
            shadow: false,
//            layout: {
//                type: 'fit'
//            },
            style:{
                // 'z-index': 1,
                'background-color':'transparent'
            },
            items: [{
                text: 'Tools',
                iconCls: 'cog',
                menu: [{text: 'Product navigator'}, {text: 'Vector layers'}, {text: 'Menu Button 3'}]
            },{
                text: 'Layers',
                iconCls: 'add16',
                menu: [{text: 'Layer 1'}, {text: 'Layer 2'}]
            },{
                text: 'Unlink',
                enableToggle: true,
                iconCls: 'add16',
                handler: 'toggleLink'
//            }, {
//                xtype: 'slider',
//                // cls: 'custom-slider',
//                hideLabel: false,
//                border: true,
//                width: 214,
//                increment: 10,
//                minValue: 0,
//                maxValue: 100
            },
            '->',
            {
                xtype: 'box',
                width: 200,
                height: 20,
                // alignTarget : this.getBody(),
                // defaultAlign : 'tr-tr',
                html: '<div id="mouse-position_' + me.id + '"></div>'
            }]
        });

        me.mapView = new ol.View({
            projection:me.epsg,
            center: ol.proj.transform([21, 4], 'EPSG:4326', 'EPSG:3857'),
            zoom: 3
        });

        me.name ='mapviewwindow_' + me.id;
        me.items = [{
            xtype:'container',
            html: '<div id="mapview_' + me.id + '"></div>'
        }, {
            xtype: 'slider',
            // cls: 'custom-slider',
            id: 'opacityslider'+ me.id,
            fieldLabel: ' ',
            labelStyle: { color:'lightgray'},
            labelSeparator: '',
            labelWidth: 40,
            hideLabel: false,
            border: true,
            autoShow: true,
            floating:true,
            // alignTarget : me,
            defaultAlign: 'tr-tr',
            alwaysOnTop: false,
            constrain: true,
            width: 220,
            value: 100,
            increment: 10,
            minValue: 0,
            maxValue: 100,
            tipText: function(thumb){
                return Ext.String.format('<b>{0}%</b>', thumb.value);
            },
            listeners: {
                change: function( slider, newValue, thumb, eOpts ){
                    console.info(me.map.getLayers());
                    var _layers = me.map.getLayers();
                    _layers.a[0].setOpacity(newValue/100)
                }
            }
        }];

        me.listeners = {
            afterrender: function () {
                var mousePositionControl = new ol.control.MousePosition({
                  coordinateFormat: ol.coordinate.createStringXY(4),
                  projection: 'EPSG:4326',
                  // comment the following two lines to have the mouse position be placed within the map.
                  // className: 'ol-full-screen',
                  // className: 'custom-mouse-position',
                  target:  document.getElementById('mouse-position_'+ me.id), // Ext.get('mouse-position_'+ me.id), //
                  undefinedHTML: '&nbsp;'
                });

                this.map = new ol.Map({
                    target: 'mapview_'+ this.id,
                    layers: this.layers,
                    view: this.up().commonMapView,
                    controls: ol.control.defaults({
                        attribution:false,
                        attributionOptions: /** @type {olx.control.AttributionOptions} */ ({
                          collapsible: true // false to show always without the icon.
                        })
                    }).extend([mousePositionControl])
                });
                this.map.getView().projection = this.epsg;

//                console.info(Ext.getCmp('opacityslider'+ this.id));
//                console.info(this.layers[0]);
//                var opacity = new ol.dom.Input(document.getElementById('opacityslider'+ this.id));
//                opacity.bindTo('value', this.layers[0], 'opacity')
//                       .transform(parseFloat, String);

            }
            // The resize handle is necessary to set the map!
            ,resize: function () {
                var size = [document.getElementById(this.id + "-body").offsetWidth, document.getElementById(this.id + "-body").offsetHeight];
                this.map.setSize(size);
            }
        };

        me.callParent();
    }
});