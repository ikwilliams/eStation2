
Ext.define("esapp.view.acquisition.DataAcquisition",{
    "extend": "Ext.grid.Panel",

    "controller": "dataacquisition",

    "viewModel": {
        "type": "dataacquisition"
    },

    "xtype"  : 'dataacquisitiongrid',

    requires: [
        'esapp.view.acquisition.DataAcquisitionModel',
        'esapp.view.acquisition.DataAcquisitionController',
        'Ext.grid.plugin.CellEditing',
//        'Ext.grid.column.Action',
//        'Ext.grid.column.Widget',
        'Ext.grid.column.Check'
    ],

//    store: 'DataAcquisitionsStore',
//    bind: '{ProductAcquisitionsGrid.selection.DataAcquisitions}',
//    bind: '{products.dataacquisitions}',
//    bind: '{dataacquisitions}',

    // get the chained store vrom view model
    bind:{
        store:'{productdatasources}'
    },

    viewConfig: {
        stripeRows: false,
        enableTextSelection: true,
        draggable: false,
        markDirty: false,
        resizable: false,
        disableSelection: true,
        trackOver: false
    },
    plugins:[{
        ptype:'cellediting'
    }],
    hideHeaders: true,
    columnLines: false,
    rowLines: false,
//    frame: false,
//    border: false,

    listeners: {
        mouseenter: {
            element: 'el',
            fn: function(){
                this.suspendEvents();
            }
        }
    },

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
//            xtype: 'actioncolumn',
//            width: 30,
//            sortable: false,
//            menuDisabled: true,
//            items: [{
//                icon: 'resources/img/icons/delete.png',
//                tooltip: 'Delete Product',
//                scope: me,
////                handler: me.onRemoveClick
//                handler: function(grid, rowIndex){
//                    Ext.toast({
//                        html: 'Removed row!',
//                        title: 'onRemoveClick',
//                        width: 200,
//                        align: 't'
//                    });
//                }
//            }]
//        }, {
//            text: '', // 'Type',
            width: 105,
            dataIndex: 'type'
//            bind: '{products.dataacquisitions.type}'
//            bind: '{dataacquisitions.type}'
        }, {
//            text: '', // 'Latest Acquired',
            width: 110,
            dataIndex: 'time_latest_copy'
//            bind: '{products.dataacquisitions.latest}'
//            bind: '{dataacquisitions.latest}'
        }, {
//            text: '', // 'Latest Acquired',
            width: 110,
            dataIndex: 'time_latest_exec'
//            bind: '{products.dataacquisitions.latest}'
//            bind: '{dataacquisitions.latest}'
        }, {
            xtype: 'checkcolumn',
//            text: '', // 'Active',
            width: 65,
            disabled: true,
            stopSelection: true,
            dataIndex: 'activated'
//            bind: '{products.dataacquisitions.activated}'
//            bind: '{dataacquisitions.activated}'
        }];

        me.callParent();
    }
});
