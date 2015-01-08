
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
        'Ext.grid.column.Action',
        'Ext.grid.column.Check'
    ],

//    store: 'DataAcquisitionsStore',
//    bind: '{ProductAcquisitionsGrid.selection.DataAcquisitions}',
//    bind: '{products.dataacquisitions}',
//    bind: '{dataacquisitions}',

    // get the chained store from view model
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
            // text: '', // 'Type',
            width: 105,
            dataIndex: 'type'
//            bind: '{products.dataacquisitions.type}'
//            bind: '{dataacquisitions.type}'
        }, {
            // text: '', // 'Latest Acquired',
            width: 110,
            dataIndex: 'time_latest_copy',
            hidden: true
//            bind: '{products.dataacquisitions.latest}'
//            bind: '{dataacquisitions.latest}'
        }, {
            // text: '', // 'Latest Acquired',
            width: 110,
            dataIndex: 'time_latest_exec',
            hidden: true
//            bind: '{products.dataacquisitions.latest}'
//            bind: '{dataacquisitions.latest}'
        }, {
            xtype: 'actioncolumn',
            // header: 'Active',
            hideable: false,
            hidden:false,
            // disabled: true,
            // stopSelection: false,
            width: 65,
            align: 'center',
            items: [{
                // scope: me,
                // handler: me.onToggleActivation
                disabled: false,
                getClass: function(v, meta, rec) {
                    if (rec.get('activated')) {
                        return 'activated';
                    } else {
                        return 'deactivated';
                    }
                },
                getTip: function(v, meta, rec) {
                    if (rec.get('activated')) {
                        return 'Deactivate Aqcuisition';
                    } else {
                        return 'Activate Aqcuisition';
                    }
                },
                handler: function(grid, rowIndex, colIndex) {
                    var rec = grid.getStore().getAt(rowIndex),
                        action = (rec.get('activated') ? 'deactivated' : 'activated');
                    Ext.toast({ html: action + ' ' + rec.get('productcode'), title: 'Action', width: 300, align: 't' });
                    rec.get('activated') ? rec.set('activated', false) : rec.set('activated', true);
                }
            }]
        }];

        me.callParent();
    }
});
