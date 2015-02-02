
Ext.define("esapp.view.acquisition.ingestionlog.LogView",{
    "extend": "Ext.window.Window",
    "controller": "acquisition-ingestionlog-logview",
    "viewModel": {
        "type": "acquisition-ingestionlog-logview"
    },

    xtype: "ingestionlogview",

    requires: [
        'esapp.view.acquisition.ingestionlog.LogViewController',

        'Ext.form.field.HtmlEditor',
        'Ext.form.field.Text',
        'Ext.layout.container.Center',
        'Ext.XTemplate'
    ],

    title: 'Ingested product log file',
    header: {
        titlePosition: 0,
        titleAlign: 'center'
    },
    modal: false,
    closable: true,
    closeAction: 'destroy', // 'hide',
    maximizable: false,
    width:1000,
    height:600,
    border:true,
    frame:true,
    layout: {
        type  : 'fit',
        padding: 5
    },
    autoScroll: true,

    record: null,

    listeners: {
            beforerender: "getFile"
    },

    initComponent: function () {
        var me = this;

        //me.listeners = {
        //    beforerender: "getFile"
        //};

        me.tbar = ['  ',
            {
                xtype: 'textfield',
                id:'highlightfindstring',
                fieldLabel: 'Search',
                labelWidth: 60,
                labelAlign: 'left',
                labelStyle: 'font-weight:bold;',
                hidden:false,
                qtip:'Search and highlight in current file.',
                width:250
//                scope:this
//                listeners: {
//                    keyup: function(txtfield, e) {
//                             console.info(this);
//                             console.info(txtfield);
//                             console.info(e);
////                             if(Ext.EventObject.ESC == e.getKey()) {
////                                field.onTriggerClick();
////                             }
////                             else {
////                                 var val = this.getRawValue();
////                                 var re = new RegExp('.*' + val + '.*', 'i');
////                             }
//                       }
//                }
            },{
                text: '',
                iconCls: 'magnifier-left-icon',
                handler: 'highlightSearchString'
            }
        ];

        me.items = [{
            xtype: 'htmleditor',
            id: 'logfilecontent',
            autoScroll: true,
            border: true,
            frame: true,
            layout: {
                type  : 'fit',
                padding: 5
            },
            enableAlignments: false,
            enableColors: true,
            enableFont: true,
            enableFontSize: true,
            enableFormat: false,
            enableLinks: false,
            enableLists: false,
            enableSourceEdit: false
        }];

        me.callParent();

    }
});
