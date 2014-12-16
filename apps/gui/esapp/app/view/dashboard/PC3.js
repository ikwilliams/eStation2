
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
    bodyCls:'active-panel-body-style',
//                cls: 'body.x-border-layout-ct, div.x-border-layout-ct',

    layout: 'border',
    bodyBorder: false,
    bodyPadding:0,
    flex:1,
    defaults: {
        bodyCls:'active-panel-body-style'
    },

    initComponent: function () {
        var me = this;

        me.bodyCls = 'active-panel-body-style';
        me.bodyPadding = 0;

        me.items = [{
            xtype: 'container',
            region: 'center',
            flex:1,
            layout: 'fit',
            bodyCls:'active-panel-body-style',
            style: {
                backgroundColor: '#FFF'
            },
            bodyPadding:3,
            html: 'Active version 2.0.1<br>PostgreSQL Status: X<br>Internet connection: X'
        },{
            region: 'south',
            split:false,
            collapsible:true,
            colappsed: true,
            flex:1,
            title: 'Disk status',
            layout: 'fit',
            bodyPadding:3,
            style: {
                backgroundColor: '#FFF'
            },
            items: [{
                xtype: 'image',
                src: 'resources/img/RAID_Monitor.png',
                colspan: 2,
                width: 265,
                height: 158
            }]

        }];

        me.callParent();
    }
});
