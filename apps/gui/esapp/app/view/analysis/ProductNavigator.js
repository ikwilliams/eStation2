
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

        'Ext.layout.container.Center',
        'Ext.grid.plugin.RowExpander',
        'Ext.XTemplate'
    ],

    title: 'Product Navigator',
    header: {
        titlePosition: 0,
        titleAlign: 'center'
    },
    modal: true,
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

    initComponent: function () {
        var me = this
            ,cfg = {productselected:false}
        ;

        Ext.apply(cfg, {
            listeners: {
                close:me.onClose
            },

            items : [{
                xtype : 'grid',
                region: 'center',
                width: 485,
                store: 'ProductsActiveStore',
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
                    rowclick: function(gridview, record){
                        //var productinfopanel = Ext.ComponentQuery.query('panel[id=ProductDataSetsInfo]')[0];
                        var productinfopanel = gridview.up().up().down('panel[id=ProductDataSetsInfo]');
                        productinfopanel.setTitle( 'Product: ' + record.data.prod_descriptive_name)
                        productinfopanel.expand(true);
                    }
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
                            width: 485,
                            dataIndex: 'prod_descriptive_name',
                            renderer : function(val) {
                                return '<b>' + val + '</b>';
                            }
                        }
                    ]
                }]
            }, {
                region: 'east',
                id: 'ProductDataSetsInfo',
                title: 'Product Info',
                autoWidth:true,
                split: true,
                collapsible: true,
                collapsed: true,
                floatable: false,
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
                items: [
                    {
                        xtype:''
                    }
                ]
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
