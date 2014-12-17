
Ext.define("esapp.view.dashboard.Dashboard",{
    "extend": "Ext.panel.Panel",

    "controller": "dashboard-dashboard",

    "viewModel": {
        "type": "dashboard-dashboard"
    },

    xtype  : 'dashboard-main',

    requires: [
        'Ext.layout.container.HBox',
        'Ext.layout.container.VBox',
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

        me.defaults = {
            titleAlign: 'center',
            frame: true,
            border: false,
            bodyPadding: 10
        };

        me.items = [{
                xtype: 'dashboard-pc1'
            }, {
                xtype: 'dashboard-connection',
                connected: true
            }, {
                xtype: 'dashboard-pc2'
            }, {
                xtype: 'dashboard-connection',
                connected: true
            }, {
                xtype: 'dashboard-pc3'
        }];

        me.callParent();
    }
});
