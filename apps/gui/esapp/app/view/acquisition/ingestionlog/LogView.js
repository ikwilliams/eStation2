
Ext.define("esapp.view.acquisition.ingestionlog.LogView",{
    "extend": "Ext.window.Window",
    "controller": "acquisition-ingestionlog-logview",
    "viewModel": {
        "type": "acquisition-ingestionlog-logview"
    },

    xtype: "ingestionlogview",

    requires: [
        'esapp.view.acquisition.ingestionlog.LogViewController',

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
    border:true,
    frame:true,
    layout: {
        type  : 'fit',
        padding: 5
    },
    autoScroll: true,

    initComponent: function () {
        var me = this;

        me.tbar = ['  ',
            {
                xtype: 'textfield',
                id:'highlightfindstring',
                fieldLabel: 'Search',
                labelStyle: 'font-weight:bold;',
                hidden:false,
                qtip:'Search in current file.',
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
                handler: function() {
                    var searchText = Ext.getCmp('highlightfindstring').getValue().trim();

                    if ( searchText != '') {
                        var targetcontent = eStation.myGlobals.OriginalContent;    // eStation.myGlobals.OriginalContent is set in logfilelist onRowAction
                        var textColor = "black";
                        var bgColor = "yellow";
                        var treatAsPhrase = false;
                        var warnOnFailure=false;
                        var highlightStartTag = "<span style='color:" + textColor + "; background-color:" + bgColor + ";'>";
                        var highlightEndTag = "</span>";

                        var highlightedcontent = highlightSearchTerms(targetcontent, searchText, treatAsPhrase, warnOnFailure, highlightStartTag, highlightEndTag);

                        var contentField = Ext.getCmp('logfilecontent');
                        Ext.getCmp('logfilecontent').setValue(highlightedcontent);

                    }
                    else Ext.getCmp('logfilecontent').setValue(eStation.myGlobals.OriginalContent);   // No search terms so reset content to original content
                }
            }
        ];

        me.items = [{
            xtype: 'htmleditor',
            id: 'logfilecontent',
            autoScroll: true,
            width: 830,
            height: 468,
            enableAlignments: false,
            enableColors: false,
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
