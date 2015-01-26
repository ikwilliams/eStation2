
Ext.define("esapp.view.acquisition.ingestionlog.LogView",{
    "extend": "Ext.window.Window",
    "controller": "acquisition-ingestionlog-logview",
    "viewModel": {
        "type": "acquisition-ingestionlog-logview"
    },

    xtype: "ingestionlogview",

    requires: [
        'Ext.layout.container.Center',

        'Ext.XTemplate'
    ],

    title: 'Ingested product log file',
    header: {
        titlePosition: 0,
        titleAlign: 'center'
    },
    modal: true,
    closable: true,
    closeAction: 'destroy', // 'hide',
    maximizable: false,
    width:850,
    height:530,
    layout: {
        type  : 'fit',
        padding: 5
    },
    autoScroll: true,


});
