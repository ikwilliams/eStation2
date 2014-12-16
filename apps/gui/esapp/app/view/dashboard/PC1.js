
Ext.define("esapp.view.dashboard.PC1",{
    "extend": "Ext.panel.Panel",
    "controller": "dashboard-pc1",
    "viewModel": {
        "type": "dashboard-pc1"
    },
    xtype  : 'dashboard-pc1',

    requires: [
        'Ext.layout.container.HBox',
        'Ext.layout.container.Column',
        'Ext.layout.container.Table',
        'Ext.layout.container.Accordion',
        'Ext.Img',
    ],

    name:'dashboardpc1',
    id: 'dashboardpc1',

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
        border: false
    },

    initComponent: function () {
        var me = this;

        me.items = [{
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
            xtype:'container',
            layout: 'accordion',
            colspan: 2,
            height: 200,
            width: '100%',
            items:[{
                xtype: 'panel', // << fake hidden panel
                hidden: true,
                collapsed: false
            },{
                title: 'Disk status',
                layout: 'hbox',
                collapsed: true,
                items: [{
                    xtype: 'image',
                    src: 'resources/img/RAID_Monitor.png',
                    colspan: 2,
                    width: 265,
                    height: 158
                }]
            }]
        }];

        me.callParent();
    }
});
