
Ext.define("esapp.view.dashboard.PC3",{
    "extend": "Ext.panel.Panel",
    "controller": "dashboard-pc3",
    "viewModel": {
        "type": "dashboard-pc3"
    },
    xtype  : 'dashboard-pc3',

    requires: [
        'Ext.layout.container.Border',
        'Ext.Img'
    ],

    name:'dashboardpc3',
    id: 'dashboardpc3',

    title: '<span class="panel-title-style">Analysis (PC3)</span>',

    disabled:false,
    activePC:false,

    layout: 'border',
    bodyBorder: true,
    bodyPadding:0,
    flex:1,

    initComponent: function () {
        var me = this;

        me.bodyPadding = 0;

        me.tbar = Ext.create('Ext.toolbar.Toolbar', {
            layout: {
                    type: 'vbox',
                    align: 'middle'
            },
            padding: '5 5 10 5',
            // cls:'active-panel-body-style',
            defaults: {
                width: 160,
                textAlign: 'left',
                disabled: true
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
                    // beforerender: 'checkStatusServices'
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
            }, '-',{
                xtype: 'splitbutton',
                name: 'datasyncbtn',
                text: 'Data Syncronization',
                iconCls: 'fa fa-cog fa-2x',  //  fa-spin 'icon-loop', // icomoon fonts
                style: { color: 'gray' },
                scale: 'medium',
                width: 215,
                handler: 'checkStatusServices',
                menu: Ext.create('Ext.menu.Menu', {
                    width: 200,
                    margin: '0 0 10 0',
                    floating: true,
                    items: [
                        {   xtype: 'checkbox',
                            boxLabel: 'Disable Auto Sync',
                            name: 'enabledisableautosync',
//                            glyph: 'xf04b@FontAwesome',
//                            cls:'menu-glyph-color-green',
                            handler: 'execEnableDisableAutoSync'
                        },
                        {   text: 'Execute Now',
                            name: 'executenow',
                            glyph: 'xf04b@FontAwesome',
                            cls:'menu-glyph-color-green',
                            handler: 'execManualSync'
                        }
                    ]
                })
            },{
                xtype: 'splitbutton',
                name: 'dbsyncbtn',
                text: 'DB Syncronization',
                iconCls: 'fa fa-cog fa-2x',  //  fa-spin 'icon-loop', // icomoon fonts
                style: { color: 'grey' },
                scale: 'medium',
                width: 215,
                handler: 'checkStatusServices',
                menu: Ext.create('Ext.menu.Menu', {
                    width: 200,
                    margin: '0 0 10 0',
                    floating: true,
                    items: [
                        {   xtype: 'checkbox',
                            boxLabel: 'Disable Auto Sync',
                            name: 'enabledisableautodbsync',
//                            glyph: 'xf04b@FontAwesome',
//                            cls:'menu-glyph-color-green',
                            handler: 'execEnableDisableAutoDBSync'
                        },
                        {   text: 'Execute Now',
                            name: 'executenow',
                            glyph: 'xf04b@FontAwesome',
                            cls:'menu-glyph-color-green',
                            handler: 'execManualDBSync'
                        }
                    ]
                })
            }]
        });

        me.items = [{
            xtype: 'panel',
            region: 'center',
            layout: {
                type: 'table',
                columns: 2,
                tableAttrs: {
                    style: {
                        width: '100%',
                        padding:0
                    }
                }
            },
            bodyPadding:10,
            items: [{
                xtype: 'container',
                html: 'Active version',
                cls: 'panel-text-style'
            },{
                xtype: 'container',
                html: '<b>2.0.1</b>'
            },{
                xtype: 'container',
                html: 'Mode:',
                cls: 'panel-text-style',
                width: 140
            },{
                xtype: 'container',
                html: '<b>Nominal mode</b>'
            },{
                xtype: 'container',
                html: 'PostgreSQL Status:',
                cls: 'panel-text-style',
                width: 140
            },{
                xtype: 'image',
                src: 'resources/img/icons/check-square-o.png'
            },{
                xtype: 'container',
                html: 'Internet connection:',
                cls: 'panel-text-style',
                width: 140
            },{
                xtype: 'image',
                src: 'resources/img/icons/check-square-o.png'
            }]
        },{
            region: 'south',
            title: '&nbsp;Disk status',
            split:false,
            collapsible:true,
            collapsed: true,
            // flex:1,
            iconCls: 'x-tool-okay', // 'fa fa-check-circle-o fa-2x', // fa-check-square fa-chevron-circle-down fa-check-circle fa-check
            iconAlign : 'left',
            height: 240,
            minHeight: 200,
            maxHeight: 240,
            layout: 'fit',
            style: {
                color: 'white'
            },
            items: [{
                xtype: 'image',
                src: 'resources/img/RAID_Monitor.png',
                width: 265,
                height: 158
            }]

        }];

        if (me.activePC) {
            me.items[0].bodyCls = 'active-panel-body-style';
        }

        me.callParent();
    }
});
