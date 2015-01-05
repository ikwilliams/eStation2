
Ext.define("esapp.view.processing.MapSetFinalOutputSubProduct",{
    "extend": "Ext.grid.Panel",
    "controller": "processing-mapsetfinaloutputsubproduct",
    "viewModel": {
        "type": "processing-mapsetfinaloutputsubproduct"
    },

    "xtype"  : 'mapset_finaloutput_subproduct_grid',

    requires: [
        'esapp.view.processing.MapSetFinalOutputSubProductModel',
        'esapp.view.processing.MapSetFinalOutputSubProductController',

        'Ext.grid.column.Action',
        'Ext.grid.column.Widget'
    ],

    store: null,

    viewConfig: {
        stripeRows: false,
        enableTextSelection: true,
        draggable: false,
        markDirty: false,
        resizable: false,
        disableSelection: true,
        trackOver: false
    },

    hideHeaders: true,
    columnLines: false,
    rowLines:false,

    initComponent: function () {
        var me = this;

        me.defaults = {
            menuDisabled: true,
            variableRowHeight : true,
            draggable:false,
            groupable:false,
            hideable: false
        };

        me.columns = [{
            header: '', // 'Sub Product Code',
            dataIndex: 'subproductcode',
            width: 180
        },{
            xtype: 'checkcolumn',
            header: '', // Active
            width: 65,
            dataIndex: 'activated',
            stopSelection: false,
            hideable: true,
            hidden: false,
            disabled: false,
            listeners: {
              checkchange: function(chkBox, rowIndex, checked, eOpts){
                  var myTitle = ""
                  if (checked)  myTitle = "Activate Processing of Final SubProduct";
                  else myTitle = "De-activate Processing of Final SubProduct";
                  Ext.toast({ html: 'Checkbox clicked!', title: myTitle, width: 200, align: 't' });
              }
            }
        }];

        me.callParent();
    }

});
