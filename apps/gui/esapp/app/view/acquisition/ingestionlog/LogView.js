
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

    initComponent: function () {
        var me = this;

        me.listeners = {
            beforerender: function(win,evt){
                //console.info(win);
                //Ext.toast({ html: 'Before render in logview', title: 'Before render', width: 200, align: 't' });
                // me.getFile(me.record);
                //console.info("following is the record in getFile: ");
                //console.info(me.record);
                //console.info(me.record.get('productcode'));
                //console.info(me.record.get('mapsetcode'));
                //console.info(me.record.get('version'));
                //console.info(me.record.get('subproductcode'));
                Ext.Ajax.request({
                   method: 'GET',
                   url:'getlogfile',
                   params:{
                       productcode:me.record.get('productcode'),
                       mapsetcode:me.record.get('mapsetcode'),
                       version:me.record.get('version'),
                       subproductcode:me.record.get('subproductcode')
                   },
                   loadMask:'Loading data...',
                   callback:function(callinfo,responseOK,response ){

                        var response_Text = response.responseText.trim();
                        Ext.getCmp('logfilecontent').setValue(response_Text);
                        //eStation.myGlobals.OriginalContent = Ext.getCmp('logfilecontent').getRawValue();
                        //eStation.LogfileShowPanel.setTitle('File: ' + record.data.filename);
                   },
                   success: function ( result, request ) {},
                   failure: function ( result, request) {}
                });
            }
        };

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
