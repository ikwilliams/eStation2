
Ext.define("esapp.view.analysis.ProductNavigator",{
    "extend": "Ext.window.Window",
    "controller": "analysis-productnavigator",
    "viewModel": {
        "type": "analysis-productnavigator"
    },
    xtype: "productnavigator",

    requires: [
        'esapp.view.analysis.ProductNavigatorModel',
        'esapp.view.analysis.ProductNavigatorController',

        'esapp.model.ProductNavigator',
        'esapp.model.ProductNavigatorMapSet',
        'esapp.model.ProductNavigatorMapSetDataSet',

        'Ext.layout.container.Center',
        'Ext.grid.plugin.RowExpander',
        'Ext.XTemplate'
    ],

    //bind: '{products}',
    //session: true,

    title: '<div class="panel-title-style">Product Navigator</div>',
    header: {
        titlePosition: 0,
        titleAlign: 'center'
    },
    modal: true,
    border:false,
    frame: false,

    closable: true,
    closeAction: 'destroy', // 'hide',
    maximizable: false,
    resizable: false,
    width: 575,
    height: 800,
    layout: {
        type  : 'border',
        padding: 5
    },
    autoScroll: false,
    productselected:false,
    tools: [
    {
        type: 'refresh',
        tooltip: 'Refresh product list',
        callback: function (productnavwin) {
            //console.info(productnavwin);
            var productnavigatorstore  = Ext.data.StoreManager.lookup('ProductNavigatorStore');

            if (productnavigatorstore.isStore) {
                productnavigatorstore.load();
            }
        }
    }],

    initComponent: function () {
        var me = this
            ,cfg = {productselected:false}
        ;

        Ext.apply(cfg, {
            listeners: {
                close: me.onClose
            },

            items : [{
                xtype : 'grid',
                reference: 'productsGrid',
                region: 'center',
                width: 485,
                //store: 'ProductNavigatorStore',
                bind: '{products}',
                session:true,

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
                frame: false,
                border: false,

                features: [{
                    id: 'selectproductcategories',
                    ftype: 'grouping',
                    groupHeaderTpl: Ext.create('Ext.XTemplate', '<div class="group-header-style">{name} ({children.length})</div>'),
                    hideGroupedHeader: true,
                    enableGroupingMenu: false,
                    startCollapsed : false,
                    groupByText: 'Product category'
                }],

                plugins: [{
                    ptype: 'rowexpander',
                    cellWrap:true,
                    layout:'fit',
                    rowBodyTpl : new Ext.XTemplate(
                        '<span class="smalltext">' +
                        '<b style="color:darkgrey">{productcode}' +
                            '<tpl if="version != \'undefined\'">',
                                ' - {version}',
                            '</tpl>',
                        '</b>' +
                        '<p>{description}</p>' +
                        '</span>'
                    )
                }],

                listeners: {
                    scope: 'controller',
                    afterrender: 'productsGridAfterrender',
                    rowclick: 'productsGridRowClick'
                },

                columns : [{
                    text: '<div class="grid-header-style">Product categories</div>',
                    menuDisabled: true,
                    defaults: {
                        sortable: false,
                        hideable: false,
                        variableRowHeight : true,
                        menuDisabled:true
                    },
                    columns: [
                        {
                            text: "Product",
                            xtype: 'templatecolumn',
                            width: 485,
                            //dataIndex: 'prod_descriptive_name',
                            tpl: '<b>{prod_descriptive_name}</b>'
                            //renderer : function(val) {
                            //    return '<b>' + val + '</b>';
                            //}
                        }
                    ]
                }]
            }, {
                region: 'east',
                id: 'ProductDataSetsInfo',
                title: '<div class="panel-title-style">Product Info</div>',
                autoWidth:true,
                split: true,
                collapsible: true,
                collapsed: true,
                floatable: false,
                defaults: {
                    margin: {top: 10, right: 10, bottom: 10, left: 10},
                    layout: {
                        type: 'vbox'
                    }
                },
                listeners: {
                    expand: function(){
                        //this.up().down('grid').setWidth(460)
                        this.setWidth(500);
                        this.up().setWidth(1075);
                    },
                    collapse: function(){
                        //this.up().down('grid').setWidth(485)
                        this.setWidth(5);
                        this.up().setWidth(575);
                    }
                },
                items: [{
                    xtype: 'fieldset',
                    title: '<div class="grid-header-style">Mapsets available</div>',
                    border: true,
                    height: 170,
                    width: 480,
                    collapsible: true,
                    defaults: {
                        labelWidth: 89,
                        anchor: '100%',
                        layout: {
                            type: 'hbox',
                            defaultMargins: {top: 0, right: 5, bottom: 0, left: 0}
                        }
                    },
                    items: [{

                    }]
                },{
                    xtype : 'grid',
                    region: 'center',
                    autoWidth: false,
                    //store: 'ProductNavigatorStore',
                    //bind: '{products}',
                    //session:true,

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
                    frame: false,
                    border: false,

                    plugins: [{
                        ptype: 'rowexpander',
                        cellWrap:true,
                        layout:'fit',
                        rowBodyTpl : new Ext.XTemplate(
                            '<span class="smalltext">' +
                            '<b style="color:darkgrey">{productcode}' +
                                '<tpl if="version != \'undefined\'">',
                                    ' - {version}',
                                '</tpl>',
                            ' - {subproductcode}',
                            '</b>' +
                            '<p>{description}</p>' +
                            '</span>'
                        )
                    }],

                    listeners: {
                        rowclick: function(gridview, record){
                            console.info(record);
                        }
                    },
                    menuDisabled: true,
                    defaults: {
                        sortable: false,
                        hideable: false,
                        variableRowHeight : true,
                        menuDisabled:true
                    },
                    columns : [{
                        text: '<div class="grid-header-style">Data set</div>',
                        width: 450,
                        //dataIndex: 'prod_descriptive_name',
                        bind: '{prod_descriptive_name}',
                        renderer : function(val) {
                            return '<b>' + val + '</b>';
                        }
                    }]

                    //xtype:'container',
                    //items: new Ext.DataView({
                    //    //store: this.store,
                    //    bind: {
                    //        boxLabel: '{productmapsets.descriptive_name}'
                    //    },
                    //    tpl: new Ext.XTemplate(
                    //        '<tpl for=".">',
                    //            '<div class="thumb-wrap" style="width:210px; float: left;">',
                    //                '<label >',
                    //                    '<tpl>',
                    //                        '<input type=radioField value={productmapsets.mapsetcode} >',
                    //                    '</tpl>',
                    //                    '{productmapsets.descriptive_name}',
                    //                '</label>',
                    //            '</div>',
                    //        '</tpl>', {
                    //    }),
                    //    overClass: 'x-view-over',
                    //    itemSelector: 'div.thumb-wrap',
                    //    autoScroll: true
                    //})
                }]
            }]
        });

        Ext.apply(me, cfg);
        me.callParent(arguments);
    }
    ,onClose: function(win, ev) {
        //if (win.changesmade){
        //    Ext.data.StoreManager.lookup('ProductsActiveStore').load();
        //}
    }
});

