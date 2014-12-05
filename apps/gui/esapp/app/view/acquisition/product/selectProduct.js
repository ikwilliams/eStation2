
Ext.define("esapp.view.acquisition.product.selectProduct",{
//    "extend": "Ext.panel.Panel",
    "extend": "Ext.window.Window",

    "controller": "acquisition-product-selectproduct",
    "viewModel": {
        "type": "acquisition-product-selectproduct"
    },
    xtype: "selectproduct",

    requires: [
        'Ext.layout.container.Center',
        'Ext.grid.plugin.CellEditing',
//        'Ext.grid.column.Widget',
//        'Ext.grid.column.Boolean',
//        'Ext.grid.column.Template',
        'Ext.grid.column.Check',
//        'Ext.button.Split',
//        'Ext.menu.Menu',
        'Ext.XTemplate',
        'Ext.grid.column.Action'
    ],

    title: 'Product selection',
    header: {
        titlePosition: 0,
        titleAlign: 'center'
    },
    modal: true,
    closable: true,
    closeAction: 'destroy', // 'hide',
    maximizable: false,
//    animateTarget: addproduct,
    width: 650,
    height: 800,
//    tools: [{type: 'pin'}],
    layout: {
        type  : 'fit',
        // align : 'stretch',
        padding: 5
    },
    autoScroll: true,

//    tbar: Ext.create('Ext.toolbar.Toolbar', {
//            items: [
//                {
//                    xtype: 'button',
//                    text: 'Select Product',
//                    name: 'selectroduct',
//                    iconCls: 'fa fa-plus-circle',
//                    style: { color: 'gray' },
//                    hidden: true,
//                    // glyph: 'xf055@FontAwesome',
//                    scale: 'small',
//                    handler: ''
//                }
//            ]
//        }),

    initComponent: function () {
        var me = this
            ,cfg = {}
        ;
        Ext.apply(cfg, {
            listeners: {
                close:me.onClose
            },

            items : [{
                xtype : 'grid',
                // flex  : 1,

                // bind: '{products}',
                store: 'ProductsInactiveStore',
                session:true,

                plugins:[{
                    ptype:'cellediting'
                }],

                // title: 'Product Selection',
                viewConfig: {
                    stripeRows: false,
                    enableTextSelection: true,
                    draggable:false,
                    markDirty: false,
                    resizable:false,
                    disableSelection: true,
                    trackOver:true
                },

                selModel : {
                    allowDeselect : true
                },

                collapsible: false,
                enableColumnMove:false,
                enableColumnResize:false,
                multiColumnSort: false,
                columnLines: false,
                rowLines: true,
                frame: true,
                border: true,


                features: [{
                    id: 'selectproductcategories',
                    ftype: 'grouping',
                    groupHeaderTpl: Ext.create('Ext.XTemplate', '<div class="group-header-style">{name} ({children.length})</div>'),
                    hideGroupedHeader: true,
                    enableGroupingMenu: false,
                    startCollapsed : false,
                    groupByText: 'Product category'
                }],

                columns : [{
                    text: '<div class="grid-header-style">Product categories</div>',
                    menuDisabled: true,
                    columns: [{
                        xtype: 'actioncolumn',
                        hidden:true,
                        width: 30,
                        align: 'center',
                        sortable: false,
                        menuDisabled: true,
                        shrinkWrap: 0,
                        items: [{
                            icon: 'resources/img/icons/edit.png',
                            // iconCls: 'fa fa-edit fa-2x', // xf044
                            // cls: 'fa fa-edit fa-2x', // xf044
                            tooltip: 'Edit Product',
                            handler: 'editProduct'
                        }]
                    }, {
                        xtype:'templatecolumn',
                        header: 'Product',
                        tpl: new Ext.XTemplate(
                                '<b>{prod_descriptive_name}</b> <br> ' +
                                '<span class="smalltext">' +
                                '<b style="color:darkgrey">{productcode}' +
                                    '<tpl if="version != \'undefined\'">',
                                        ' - {version}',
                                    '</tpl>',
                                '</b>' +
                                '<p>{description}</p>' +
                                '</span>'
                            ),
                        width: 500,
                        cellWrap:true,
                        sortable: false,
                        hideable: false,
                        variableRowHeight : true,
                        menuDisabled:true
                    }, {
                        xtype: 'checkcolumn',
                        header: 'Active',
                        width: 80,
                        sortable: false,
                        dataIndex: 'activated',
                        stopSelection: false,
                        disabled: false,
                        menuDisabled:true,
                        listeners: {
                          checkchange: function(chkBox, rowIndex, checked, eOpts){
        //                      console.info(chkBox);
        //                      console.info(rowIndex);
        //                      console.info(checked);
        //                      console.info(eOpts);
                          }
                        }
                    }]
                }]
//            },{
//                html : 'product details with acquisition and ingestion assignments',
//                flex  : 1
            }]
        });

        Ext.apply(me, cfg);
        me.callParent(arguments);
    }
    ,onClose: function(win, ev) {
        // var acq_main = Ext.ComponentQuery.query('panel[name=acquisitionmain]');
        // acq_main.store.load();
        Ext.data.StoreManager.lookup('ProductsActiveStore').load();
    }
});
