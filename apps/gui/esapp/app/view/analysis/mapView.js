
Ext.define("esapp.view.analysis.mapView",{
    "extend": "Ext.window.Window",
    "controller": "analysis-mapview",
    "viewModel": {
        "type": "analysis-mapview"
    },
    xtype: 'mapview-window',

    requires: [
        'esapp.view.analysis.mapViewModel',
        'esapp.view.analysis.mapViewController',
        'esapp.view.widgets.TimeLine',

        'Ext.window.Window',
        'Ext.toolbar.Toolbar',
        'Ext.slider.Single'
    ],

    //title: '<span class="panel-title-style">MAP title</span>',
    margin: '0 0 0 0',
    layout: {
        type: 'border'
    },
    width:650,
    height:600,
    minWidth:400,
    minHeight:350,
    // glyph : 'xf080@FontAwesome',
    constrain: true,
    autoShow : false,
    closeable: true,
    closeAction: 'destroy', // 'hide',
    maximizable: true,
    collapsible: true,

    layers: [],
    projection: 'EPSG:4326',

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

        me.frame = false;
        me.border= false;
        me.bodyBorder = false;

        me.tbar = Ext.create('Ext.toolbar.Toolbar', {
            dock: 'top',
            autoShow: true,
            alwaysOnTop: true,
            floating: false,
            hidden: false,
            border: false,
            shadow: false,
            //style: 'background: transparent',
            bodyStyle: 'background: transparent;',
            style:{
                backgroundColor:'transparent'
            },
            items: [{
                text: 'Product navigator',
                iconCls: 'africa',
                scale: 'medium',
                handler: 'openProductNavigator'
            },{
                //text: 'Add Layer',
                iconCls: 'layers',
                scale: 'medium'
            },{
                //text: 'Unlink',
                enableToggle: true,
                iconCls: 'unlink',
                scale: 'medium',
                handler: 'toggleLink'
            },
            {
                xtype: 'box',
                width: 120,
                height: 20,
                align:'left',
                // alignTarget : this.getBody(),
                // defaultAlign : 'tr-tr',
                html: '<div id="mouse-position_' + me.id + '"></div>'
            }]
        });

        //me.bbar = {
        //    dock: 'bottom',
        //    autoShow: true,
        //    autoWidth:true,
        //    alwaysOnTop: true,
        //    hidden: true,
        //    hideMode : 'display',
        //    border: false,
        //    shadow: false,
        //    style:{
        //        backgroundColor:'transparent'
        //    },
        //    items: [{
        //        xtype: 'box',
        //        id: 'product-time-line_' + me.id,
        //        align:'left',
        //        autoWidth:true,
        //        margin:0,
        //        height: 115
        //        //html: '<div id="product-time-line_' + me.id + '">Time line here</div>'
        //    }]
        //};

        me.mapView = new ol.View({
//            projection:me.projection,
            center: ol.proj.transform([21, 4], 'EPSG:4326', 'EPSG:3857'),
            zoom: 2
        });

        me.name ='mapviewwindow_' + me.id;

        me.items = [{
            region: 'center',
            items: [{
                xtype: 'container',
                html: '<div id="mapview_' + me.id + '"></div>'
            }, {
                xtype: 'slider',
                // cls: 'custom-slider',
                id: 'opacityslider' + me.id,
                fieldLabel: '',
                labelStyle: {color: 'lightgray'},
                labelSeparator: ' ',
                labelWidth: 40,
                hideLabel: false,
                hideEmptyLabel: false,
                border: false,
                autoShow: true,
                floating: true,
                // alignTarget : me,
                defaultAlign: 'tr-c?',
                alwaysOnTop: false,
                constrain: true,
                width: 220,
                value: 100,
                increment: 10,
                minValue: 0,
                maxValue: 100,
                tipText: function (thumb) {
                    return Ext.String.format('<b>{0}%</b>', thumb.value);
                },
                listeners: {
                    change: function (slider, newValue, thumb, eOpts) {
                        //                    console.info(me.map.getLayers());
                        var _layers = me.map.getLayers();
                        _layers.a[0].setOpacity(newValue / 100)
                    }
                }
            }]
        },{
            region: 'south',
            //xtype: 'panel',
            id: 'product-time-line_' + me.id,
            reference: 'product-time-line_' + me.id,
            //title: 'Time Line',
            align:'left',
            autoWidth:true,
            margin:0,
            height: 115,
            maxHeight: 115,
            hidden: true,
            hideMode : 'display',
            frame:  false,
            border: false,
            bodyBorder: false,
            shadow: false,

            header : false,
            collapsible: true,
            collapsed: true,
            collapseFirst: true,
            collapseDirection: 'top',
            collapseMode : "mini",  // The Panel collapses without a visible header.
            //headerPosition: 'left',
            hideCollapseTool: true,
            split: true,
            splitterResize : false,
            items: [{
            //    xtype: 'container',
            //    width: 15
            //}, {
                xtype: 'time-line-chart',
                id: 'time-line-chart' + me.id,
                reference: 'time-line-chart' + me.id,
                layout: 'fit'
            //},{
            //    xtype: 'container',
            //    width: 15
            }]
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
                //console.info(me.getController());
                //this.layers = me.getController().addProductLayer();
                this.map = new ol.Map({
                    target: 'mapview_'+ this.id,
                    projection:me.projection,
                    displayProjection:"EPSG:4326",
                    //layers: this.layers,
                    view: this.up().commonMapView,
                    controls: ol.control.defaults({
                        attribution:false,
                        attributionOptions: /** @type {olx.control.AttributionOptions} */ ({
                            collapsible: true // false to show always without the icon.
                        })
                    }).extend([mousePositionControl])
                });
//                this.map.getView().projection = me.projection;

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

                this.getController().redrawTimeLine();
            }
            ,expand: function () {
                var size = [document.getElementById(this.id + "-body").offsetWidth, document.getElementById(this.id + "-body").offsetHeight];
                this.map.setSize(size);
                this.getController().redrawTimeLine();
            }
            ,move: function () {
                this.getController().redrawTimeLine();
            }

        };

        me.callParent();
    }
});
