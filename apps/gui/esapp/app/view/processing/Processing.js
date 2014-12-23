
Ext.define("esapp.view.processing.Processing",{
    "extend": "Ext.grid.Panel",
    "controller": "processing-processing",
    "viewModel": {
        "type": "processing-processing"
    },
    xtype  : 'processing-main',

    name:'processingmain',

    requires: [
        'Ext.grid.column.Widget',
        'Ext.grid.column.Template',
        'Ext.grid.column.Check',
        'Ext.button.Split',
        'Ext.menu.Menu',
        'Ext.XTemplate'
    ],

    store: 'ProcessingStore',

    // title: 'Processing Dashboard',
    viewConfig: {
        stripeRows: false,
        enableTextSelection: true,
        draggable:false,
        markDirty: false,
        resizable:false,
        disableSelection: true,
        trackOver:true
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
        id: 'processprodcat',
        ftype: 'grouping',
        groupHeaderTpl: Ext.create('Ext.XTemplate', '<div class="group-header-style">{name} ({children.length})</div>'),
        hideGroupedHeader: true,
        enableGroupingMenu: false,
        startCollapsed : false,
        groupByText: 'Product category'
    }],

    initComponent: function () {
        var me = this;

        me.tbar = Ext.create('Ext.toolbar.Toolbar', {
            items: [{
                text: 'Expand All',
                handler: function(btn) {
                    var view = btn.up().up().getView();
                    view.getFeature('processprodcat').expandAll();
                    view.refresh();
                }
            }, {
                text: 'Collapse All',
                handler: function(btn) {
                    var view = btn.up().up().getView();
                    view.getFeature('processprodcat').collapseAll();
                    view.refresh();
                }
            },
            '->',
            {
                xtype: 'button',
                iconCls: 'fa fa-refresh fa-2x',
                style: { color: 'gray' },
                enableToggle: false,
                scale: 'medium',
                handler:  function(btn) {
                    var processingstore  = Ext.data.StoreManager.lookup('ProcessingStore');

                    if (processingstore.isStore) {
                        processingstore.load();
                    }
                }
            }]
        });

        me.defaults = {
            variableRowHeight : true,
            menuDisabled: true,
            sortable: false,
            groupable:true,
            draggable:false,
            hideable: true
        };

        me.columns = [
        {
            header: '<div class="grid-header-style">Product categories</div>',
            menuDisabled: true,
            variableRowHeight : true,
            defaults: {
                menuDisabled: true,
                variableRowHeight : true,
                sortable: false,
                groupable:true,
                draggable:false,
                hideable: true
            },
            columns: [{
                xtype:'templatecolumn',
                header: 'Product',
                tpl: new Ext.XTemplate(
                        '<b>{prod_descriptive_name}</b><br>' +
                        '<span class="smalltext">' +
                        '<b style="color:darkgrey">{productcode}' +
                            '<tpl if="version != \'undefined\'">',
                                ' - {version}',
                            '</tpl>',
                        '</b>' +
                        '<p>{description}</p>' +
                        '</span><br>'
                    ),
                width: 450,
                cellWrap:true
            }]
        }, {
            header:  '<div class="grid-header-style">Processing outputs</div>',
            menuDisabled: true,
            variableRowHeight : true,
            defaults: {
                menuDisabled: true,
                variableRowHeight : true,
                sortable: false,
                groupable:true,
                draggable:false,
                hideable: true
            }
            ,columns: [{
                xtype: 'widgetcolumn',
                width: 500,
                bodyPadding:0,

                header: ' <div class="x-column-header  x-column-header-align-left x-box-item x-column-header-default x-unselectable" style="border-top: 0px; width: 215px; left: 0px; tabindex="-1">' +
                '           <div data-ref="titleEl" class="x-column-header-inner">' +
                '               <span data-ref="textEl" class="x-column-header-text">Mapset</span>' +
                '           </div>' +
                '       </div>' +
                '       <div class="x-column-header x-column-header-align-left x-box-item x-column-header-default x-unselectable" style="border-top: 0px; width: 215px; right: auto; left: 215px; margin: 0px; top: 0px;" tabindex="-1">' +
                '           <div data-ref="titleEl" class="x-column-header-inner">' +
                '               <span data-ref="textEl" class="x-column-header-text">Sub Product</span>' +
                '           </div>' +
                '       </div>' +
                '       <div class="x-column-header x-column-header-align-left x-box-item x-column-header-default x-unselectable" style="border-top: 0px; border-right: 0px; width: 70px;  left: 430px; margin: 0px; top: 0px;" tabindex="-1">' +
                '           <div data-ref="titleEl" class="x-column-header-inner">' +
                '               <span data-ref="textEl" class="x-column-header-text">Active</span>' +
                '           </div>' +
                '       </div>',
                listeners: {
                  render: function(column){
                      column.titleEl.removeCls('x-column-header-inner');
                  }
                },
                onWidgetAttach: function(widget, record) {
                    Ext.suspendLayouts();
                    var productmapsets = record.getData().productmapsets;
                    var newstore = Ext.create('Ext.data.JsonStore', {
                        model: 'ProductMapSet',
                        data: productmapsets
                    });
                    widget.setStore(newstore);
                    Ext.resumeLayouts(true);
                },
                widget: {
                    xtype: 'process-productmapsetgrid'
                }
            }]
        }];

        me.callParent();
    }
});