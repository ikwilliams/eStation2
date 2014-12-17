
Ext.define("esapp.view.dashboard.PC2",{
    "extend": "Ext.panel.Panel",
    "controller": "dashboard-pc2",
    "viewModel": {
        "type": "dashboard-pc2"
    },
    xtype  : 'dashboard-pc2',

    requires: [
        'Ext.layout.container.VBox',
        'Ext.layout.container.Column',
        'Ext.layout.container.Table',
        'Ext.toolbar.Spacer',
        'Ext.Img',
        'Ext.button.Split',
        'Ext.menu.Menu'
    ],

    name:'dashboardpc2',
    id: 'dashboardpc2',

    title: '<span class="panel-title-style">Processing (PC2)</span>',
    flex: 1,
    margin: '0 0 0 0',
    bodyCls:'active-panel-body-style',
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


    initComponent: function () {
        var me = this;

        me.tbar = Ext.create('Ext.toolbar.Toolbar', {
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

        me.items = [{
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
        }];

        me.callParent();
    }
});
