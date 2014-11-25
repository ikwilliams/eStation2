
Ext.define("esapp.view.dashboard.Dashboard",{
    "extend": "Ext.panel.Panel",

    "controller": "dashboard-dashboard",

    "viewModel": {
        "type": "dashboard-dashboard"
    },

    xtype  : 'dashboard-main',

    requires: [
        'Ext.layout.container.HBox',
        'Ext.layout.container.Column',
        'Ext.layout.container.Table',
        'Ext.toolbar.Spacer',
        'Ext.Img',
        'Ext.button.Split',
        'Ext.menu.Menu',
        'Ext.XTemplate'
    ],

    name:'dashboardmain',
    id: 'dashboard-panel',

    title: '<span class="dashboard-header-title-style">MESA Full eStation</span>',
    titleAlign: 'center',
    header: {
        cls: 'dashboard-header-style'
    },

    width: 1200,
    height: 600,

    layout: {
        type: 'hbox',
        pack: 'start',
        align: 'stretch'
    },
    frame: false,
    border: false,
    bodyPadding: '50 40 40 40',

    initComponent: function () {
        var me = this;

        var tbar = Ext.create('Ext.toolbar.Toolbar', {
            layout: {
                    type: 'vbox',
                    // pack: 'left',
                    align: 'middle'
            },
            padding: '5 5 10 5',
            cls:'active-panel-body-style',
            defaults: {
                width: 160,
                textAlign: 'left'
            },
            items: [
            {
                xtype: 'splitbutton',
                name: 'eumetcastbtn',
                text: 'EumetCast',
                iconCls: 'fa fa-cog fa-2x', // fa-spin 'icon-play', // icomoon fonts
                style: { color: 'gray' },
                // glyph: 'xf0c7@FontAwesome',
                scale: 'medium',
                handler: 'checkStatusServices',
                listeners : {
                    beforerender: 'checkStatusServices'
                },
                menu: Ext.create('Ext.menu.Menu', {
                    width: 100,
                    margin: '0 0 10 0',
                    floating: true,  // usually you want this set to True (default)
                    items: [
                        // these will render as dropdown menu items when the arrow is clicked:
                        {   text: 'Run',
                            name: 'runeumetcast',
                            // iconCls: 'fa-play-circle-o', // xf01d   // fa-play xf04b
                            glyph: 'xf04b@FontAwesome',
                            cls:'menu-glyph-color-green',
                            // style: { color: 'green' },
                            handler: 'execServiceTask'
                        },
                        {   text: 'Stop',
                            name: 'stopeumetcast',
                            // iconCls: 'fa fa-stop',
                            glyph: 'xf04d@FontAwesome',
                            cls:'menu-glyph-color-red',
                            // style: { color: 'red' },
                            handler: 'execServiceTask'
                        },
                        {   text: 'Restart',
                            name: 'restarteumetcast',
                            // iconCls: 'fa fa-refresh',
                            glyph: 'xf021@FontAwesome',
                            cls:'menu-glyph-color-orange',
                            // style: { color: 'orange' },
                            handler: 'execServiceTask'
                        }
                    ]
                })
            }, ' ',
            {
                xtype: 'splitbutton',
                name: 'internetbtn',
                text: 'Internet',
                iconCls: 'fa fa-cog fa-2x',  // 'icon-stop', // icomoon fonts
                style: { color: 'gray' },
                // glyph: 0xf05a,
                scale: 'medium',
                handler: 'checkStatusServices',
                menu: Ext.create('Ext.menu.Menu', {
                    width: 100,
                    margin: '0 0 10 0',
                    floating: true,  // usually you want this set to True (default)
                    items: [
                        // these will render as dropdown menu items when the arrow is clicked:
                        {   text: 'Run',
                            name: 'runinternet',
                            // iconCls: 'fa-play-circle-o', // xf01d   // fa-play xf04b
                            glyph: 'xf04b@FontAwesome',
                            cls:'menu-glyph-color-green',
                            // style: { color: 'green' },
                            handler: 'execServiceTask'
                        },
                        {   text: 'Stop',
                            name: 'stopinternet',
                            // iconCls: 'fa fa-stop',
                            glyph: 'xf04d@FontAwesome',
                            cls:'menu-glyph-color-red',
                            // style: { color: 'red' },
                            handler: 'execServiceTask'
                        },
                        {   text: 'Restart',
                            name: 'restartinternet',
                            // iconCls: 'fa fa-refresh',
                            glyph: 'xf021@FontAwesome',
                            cls:'menu-glyph-color-orange',
                            // style: { color: 'orange' },
                            handler:'execServiceTask'
                        }
                    ]
                })
            }, ' ', {
                xtype: 'splitbutton',
                name: 'ingestbtn',
                text: 'Ingest',
                iconCls: 'fa fa-cog fa-2x',  //  fa-spin 'icon-loop', // icomoon fonts
                style: { color: 'gray' },
                // glyph: 'e600@icomoon',
                scale: 'medium',
                handler: 'checkStatusServices',
                menu: Ext.create('Ext.menu.Menu', {
                    width: 100,
                    margin: '0 0 10 0',
                    floating: true,  // usually you want this set to True (default)
                    items: [
                        // these will render as dropdown menu items when the arrow is clicked:
                        {   text: 'Run',
                            name: 'runintgest',
                            // iconCls: 'fa-play-circle-o', // xf01d   // fa-play xf04b
                            glyph: 'xf04b@FontAwesome',
                            cls:'menu-glyph-color-green',
                            // style: { color: 'green' },
                            handler: 'execServiceTask'
                        },
                        {   text: 'Stop',
                            name: 'stopingest',
                            // iconCls: 'fa fa-stop',
                            glyph: 'xf04d@FontAwesome',
                            cls:'menu-glyph-color-red',
                            // style: { color: 'red' },
                            handler: 'execServiceTask'
                        },
                        {   text: 'Restart',
                            name: 'restartingest',
                            // iconCls: 'fa fa-refresh',
                            glyph: 'xf021@FontAwesome',
                            cls:'menu-glyph-color-orange',
                            // style: { color: 'orange' },
                            handler: 'execServiceTask'
                        }
                    ]
                })
            }, ' ', {
                xtype: 'splitbutton',
                name: 'processingbtn',
                text: 'Processing',
                iconCls: 'fa fa-cog fa-2x',  //  fa-spin 'icon-loop', // icomoon fonts
                style: { color: 'gray' },
                // glyph: 'e600@icomoon',
                scale: 'medium',
                handler: 'checkStatusServices',
                menu: Ext.create('Ext.menu.Menu', {
                    width: 100,
                    margin: '0 0 10 0',
                    floating: true,  // usually you want this set to True (default)
                    items: [
                        // these will render as dropdown menu items when the arrow is clicked:
                        {   text: 'Run',
                            name: 'runprocessing',
                            // iconCls: 'fa-play-circle-o', // xf01d   // fa-play xf04b
                            glyph: 'xf04b@FontAwesome',
                            cls:'menu-glyph-color-green',
                            // style: { color: 'green' },
                            handler: 'execServiceTask'
                        },
                        {   text: 'Stop',
                            name: 'stopprocessing',
                            // iconCls: 'fa fa-stop',
                            glyph: 'xf04d@FontAwesome',
                            cls:'menu-glyph-color-red',
                            // style: { color: 'red' },
                            handler: 'execServiceTask'
                        },
                        {   text: 'Restart',
                            name: 'restartprocessing',
                            // iconCls: 'fa fa-refresh',
                            glyph: 'xf021@FontAwesome',
                            cls:'menu-glyph-color-orange',
                            // style: { color: 'orange' },
                            handler: 'execServiceTask'
                        }
                    ]
                })
            }]
        });

        me.defaults = {
            titleAlign: 'center',
            frame: true,
            border: false,
            bodyPadding: 10
        };

        me.items = [{
                xtype: 'panel',
                title: '<span class="panel-title-style">Acquisition (PC1)</span>',
                flex: 1,
                disabled:false,
                margin: '0 0 0 0',
                layout: {
                    type: 'table',
                    columns: 2,
                    tableAttrs: {
                        style: {
                            width: '100%'
                        }
                    }
                },
                defaults: {
//                    bodyPadding: '15 20',
                    border: false
//                    ,cls: 'panel-text-style'
                },
                items: [{
                    html: 'UPS/power status',
                    cls: 'panel-text-style',
                    colspan:2
                },{
                    html: 'Power source:',
                    width: '70%'
                },{
                    html: 'AC Utility'
                },{
                    html: 'Battery Capacity:',
                    align: 'right'
                },{
                    layout: 'column',
                    height: 50,
                    items: [{
                        html: '<br>80%',
                        align: 'center'
                    },{
                        xtype: 'image',
                        src: 'resources/img/battery/BatteryBG_14.png', // Battery cilinder icon
                        width: 64,
                        height: 32
                    }]
                },{
                    html: 'Estimated Runtime:',
                    align: 'right'
                },{
                    layout: 'column',
                    height: 30,
                    items: [{
                        html: '240 min &nbsp&nbsp'
                    },{
                        xtype: 'image',
                        src: 'resources/img/icons/clock-o.png'
                    }]
                },{
                    html: '<br><br><br>Disk status:',
                    colspan: 2
                },{
                    xtype: 'image',
                    src: 'resources/img/RAID_Monitor.png',
                    colspan: 2,
                    width: 265,
                    height: 158
                }]
            }, {
                xtype: 'container',
                layout: {
                    type: 'hbox',
                    pack: 'start',
                    align: 'middle'
                },
                width: 100,
                margin: '0 0 0 0',
                defaults: {
                    width:35
                },
                items: [{
                    xtype: 'image',
                    glyph: 'xf0e7@FontAwesome', // 'fa-flash'
                    cls:'glyph-color-green fa-rotate-270 fa-3x'
                },{
                    xtype: 'image',
                    glyph: 'xf0c1@FontAwesome', // 'fa-chain'
                    cls:'glyph-color-green fa-flip-horizontal fa-3x'
                },{
                    xtype: 'image',
                    glyph: 'xf0e7@FontAwesome', // 'fa-flash'
                    cls:'glyph-color-green fa-rotate-90 fa-3x'
                }]
            }, {
                xtype: 'panel',
                title: '<span class="panel-title-style">Processing (PC2)</span>',
                flex: 1,
                margin: '0 0 0 0',
                tbar: tbar,
                bodyCls:'active-panel-body-style',
                // cls: 'boxrounded',
                defaults: {
                    bodyCls:'active-panel-body-style',
                    border: false
                },
                layout: {
                    type: 'table',
                    columns: 2,
                    tableAttrs: {
                        style: {
                            width: '100%'
                        }
                    }
                },
                items: [{
                    html: 'Active version 2.0.1',
                    colspan: 2
                },{
                    html: 'PostgreSQL Status:',
                    width: 120
                },{
                    xtype: 'image',
                    src: 'resources/img/icons/check-square-o.png'
                },{
                    html: 'Internet connection:',
                    width: 120
                },{
                    xtype: 'image',
                    src: 'resources/img/icons/times-circle-o.png'
                },{
                    html: '<br>Disk status:',
                    colspan: 2
                },{
                    xtype: 'image',
                    src: 'resources/img/RAID_Monitor.png',
                    colspan: 2,
                    width: 265,
                    height: 158
                }]
            }, {
                xtype: 'container',
                layout: {
                    type: 'hbox',
                    pack: 'start',
                    align: 'middle'
                },
                width: 100,
                margin: '0 0 0 0',
                defaults: {
//                    height: 80
                    width:35
                },
                items: [{
                    xtype: 'image',
                    glyph: 'xf0e7@FontAwesome', // 'fa-flash'
                    cls:'glyph-color-red fa-rotate-270 fa-3x'
                },{
                    xtype: 'image',
                    glyph: 'xf127@FontAwesome', // 'fa-chain-broken'
                    cls:'glyph-color-red fa-flip-horizontal fa-3x'
                },{
                    xtype: 'image',
                    glyph: 'xf0e7@FontAwesome', // 'fa-flash'
                    cls:'glyph-color-red fa-rotate-90 fa-3x'
                }]
            }, {
                xtype: 'panel',
                title: '<span class="panel-title-style">Analysis (PC3)</span>',
                flex: 1,
                disabled:true,
                items: [{
                    html: 'Active version 2.0.1<br>PostgreSQL Status: X<br>Internet connection: X'
                }]
        }];

        me.callParent();
    }
});
