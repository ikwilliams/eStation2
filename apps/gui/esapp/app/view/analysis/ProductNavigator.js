
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
        'Ext.XTemplate',
        'Ext.form.RadioGroup'
    ],

    //bind: '{products}',
    //session: true,

    title: '<div class="panel-title-style-16">Product Navigator</div>',
    header: {
        titlePosition: 0,
        titleAlign: 'center',
        iconCls: 'africa'
    },

    modal: true,
    border:false,
    frame: false,

    closable: true,
    closeAction: 'hide', // 'destroy',
    tools: [
    {
        type: 'refresh',
        align: 'c-c',
        tooltip: 'Refresh product list',
        callback: 'refreshProductsGrid'
    }],

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
    mapviewid:null,

    initComponent: function () {
        var me = this
            ,cfg = {productselected:false}
        ;

        Ext.apply(cfg, {
            id: me.mapviewid+'-productnavigator',

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
                    reference: 'selectproductcategories',
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
                        '<p>{description}</p>' +
                        '</span>'
                    )
                }],

                listeners: {
                    //scope: 'controller',
                    afterrender: 'refreshProductsGrid', // 'loadProductsStore',
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
                            tpl:  new Ext.XTemplate(
                                '<b>{prod_descriptive_name}' +
                                '<tpl if="version != \'undefined\'">',
                                    ' - {version}',
                                '</tpl>',
                                '</b></br><span class="smalltext">' +
                                '<b style="color:darkgrey">{productcode}</b>' +
                                '</span>'
                            )
                            //dataIndex: 'prod_descriptive_name',
                            //renderer : function(val) {
                            //    return '<b>' + val + '</b>';
                            //}
                        }
                    ]
                }]
            }, {
                region: 'east',
                reference: 'product-datasets-info',
                title: '<div class="panel-title-style-16">Product Info</div>',
                header: {
                    titlePosition: 0,
                    titleAlign: 'left',
                    height: 33
                    //,style: {backgroundColor:'#ADD2ED'}
                },
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
                        this.setWidth(550);
                        this.up().setPosition(370,140);
                        this.up().setWidth(1100);
                    },
                    collapse: function(){
                        //this.up().down('grid').setWidth(485)
                        this.setWidth(5);
                        this.up().setPosition(670,140);
                        this.up().setWidth(575);
                    }
                },
                items: [{
                    xtype: 'fieldset',
                    title: '<div class="grid-header-style">Mapsets available</div>',
                    reference: 'product-mapsets-dataview',
                    border: true,
                    height: 220,
                    width: 530,
                    collapsible: false,
                    layout: 'fit',
                    padding: {top: 5, right: 5, bottom: 0, left: 5},
                    items: Ext.create('Ext.view.View', {
                        bind: '{productmapsets}',
                        //id: 'mapsets',
                        //boxLabel: '{descriptive_name}',
                        tpl: Ext.create('Ext.XTemplate',
                            '<tpl for=".">',
                                '<div class="mapset" id="{mapsetcode:stripTags}">',
                                    '<img src="{footprint_image}" title="{descriptive_name:htmlEncode}">',
                                    '<span><strong>{descriptive_name:htmlEncode}</strong></span>',
                                '</div>',
                            '</tpl>',
                            '<div class="x-clear"></div>'
                        ),
                        multiSelect: false,
                        height: 250,
                        width: 140,
                        trackOver: true,
                        cls:'mapsets',
                        overItemCls: 'mapset-hover',
                        itemSelector: 'div.mapset',
                        emptyText: 'No mapsets to display. Please select a product to view its mapsets',
                        autoScroll: true,
                        listeners: {
                            itemclick: 'mapsetItemClick'
                        }
                    })
                },{
                    xtype : 'grid',
                    reference: 'mapset-dataset-grid',
                    region: 'center',
                    autoWidth: false,
                    height: 300,
                    hidden: true,
                    //store: 'ProductNavigatorStore',
                    bind: '{mapsetdatasets}',
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
                        variableRowHeight : false,
                        menuDisabled:true
                    },
                    columns : [{
                        text: '<div class="grid-header-style">Data sets</div>',
                        xtype: 'templatecolumn',
                        tpl: '<b>{descriptive_name}</b>',
                        width: 455,
                        sortable: false,
                        menuDisabled:true
                        //dataIndex: 'descriptive_name',
                        //bind: '{descriptive_name}',
                        //renderer : function(val) {
                        //    return '<b>' + val + '</b>';
                        //}
                    }]
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

