
Ext.define("esapp.view.acquisition.Acquisition",{
    extend: "Ext.grid.Panel",

    controller: "acquisition",

    viewModel: {
        type: "acquisition"
    },

    xtype  : 'acquisition-main',

    requires: [
        // 'esapp.model.*',
        'Ext.layout.container.Center',
        'Ext.grid.plugin.CellEditing',
        'Ext.grid.column.Widget',
        'Ext.grid.column.Boolean',
        'Ext.grid.column.Template',
        'Ext.grid.column.Check',
        'Ext.button.Split',
        'Ext.menu.Menu',
        'Ext.XTemplate',
        'Ext.grid.column.Action'
    ],

    name:'acquisitionmain',

    store: 'ProductsActiveStore',
//    referenceHolder: true,
//    reference: 'ProductAcquisitionsGrid',
//    bind: {
//        store:'{products}'
//    },
//    bind:'{products}',
//    session:true,

    // title: 'Product Acquisition Dashboard',
    viewConfig: {
        stripeRows: false,
        enableTextSelection: true,
        draggable:false,
        markDirty: false,
        resizable:false,
        disableSelection: true,
        trackOver:true
    },

    // selModel : {
    //    allowDeselect : false
    // },

    collapsible: false,
    // suspendLayout:true,
    enableColumnMove:false,
    enableColumnResize:false,
    multiColumnSort: false,
    columnLines: false,
    rowLines: true,
    frame: false,
    border: false,

    features: [{
        id: 'productcategories',
        ftype: 'grouping',
        groupHeaderTpl: Ext.create('Ext.XTemplate', '<div class="group-header-style">{name} ({children.length})</div>'),
        hideGroupedHeader: true,
        enableGroupingMenu: false,
        startCollapsed : false,
        groupByText: 'Product category'
    }],

    plugins:[{
//        ptype:'lazyitems'
//    },{
        ptype:'cellediting'
    }],

    // defaultListenerScope: true,

    initComponent: function () {
        var me = this;

        me.tbar = Ext.create('Ext.toolbar.Toolbar', {
            items: [{
                xtype: 'button',
                name: 'lockunlock',
                iconCls: 'fa fa-lock fa-2x',  // 'fa-unlock' = xf09c  'fa-lock' = xf023
                // style: { color: 'gray' },
                // glyph: 'xf023@FontAwesome',
                enableToggle: true,
                scale: 'medium',
                handler:  function(btn) {

                    Ext.suspendLayouts();

                    var acq_main = Ext.ComponentQuery.query('panel[name=acquisitionmain]');
                    var dataacquisitiongrids = Ext.ComponentQuery.query('dataacquisitiongrid');
                    var addproductbtn = Ext.ComponentQuery.query('panel[name=acquisitionmain] > toolbar > button[name=addproduct]');
                    var checkColumns = Ext.ComponentQuery.query('panel[name=acquisitionmain] checkcolumn, dataacquisitiongrid checkcolumn, ingestiongrid checkcolumn');
                    var actionColumns = Ext.ComponentQuery.query('panel[name=acquisitionmain] actioncolumn, dataacquisitiongrid actioncolumn, ingestiongrid actioncolumn');

                    if (btn.pressed){
                        // ToDo: check if logged in!

                        acq_main[0].columns[3].setWidth(420);
                        acq_main[0].columns[3].setText(' <div class="x-column-header x-column-header-align-left x-box-item x-column-header-default x-unselectable x-column-header-first" style="border-top: 0px; width: 111px; left: 0px; tabindex="-1">' +
                        '           <div data-ref="titleEl" class="x-column-header-inner">' +
                        '               <span data-ref="textEl" class="x-column-header-text">Type</span>' +
                        '           </div>' +
                        '       </div>' +
                        '       <div class="x-column-header x-column-header-align-left x-box-item x-column-header-default x-unselectable" style="border-top: 0px; width: 110px; right: auto; left: 111px; margin: 0px; top: 0px;" tabindex="-1">' +
                        '           <div data-ref="titleEl" class="x-column-header-inner">' +
                        '               <span data-ref="textEl" class="x-column-header-text">Last copied</span>' +
                        '           </div>' +
                        '       </div>' +
                        '       <div class="x-column-header x-column-header-align-left x-box-item x-column-header-default x-unselectable" style="border-top: 0px; width: 110px; right: auto; left: 221px; margin: 0px; top: 0px;" tabindex="-1">' +
                        '           <div data-ref="titleEl" class="x-column-header-inner">' +
                        '               <span data-ref="textEl" class="x-column-header-text">Last executed</span>' +
                        '           </div>' +
                        '       </div>' +
                        '       <div class="x-column-header x-column-header-align-left x-box-item x-column-header-default x-unselectable" style="border-top: 0px; border-right: 0px; width: 60px; left: 332px; margin: 0px; top: 0px;" tabindex="-1">' +
                        '           <div data-ref="titleEl" class="x-column-header-inner">' +
                        '               <span data-ref="textEl" class="x-column-header-text">Active</span>' +
                        '           </div>' +
                        '       </div>');

                        addproductbtn[0].show();
                        acq_main[0].columns[0].show();  // Last copied
                        acq_main[0].columns[2].show();  // Last executed
                        Ext.Object.each(dataacquisitiongrids, function(id, dataacquisitiongrid, myself) {
                            dataacquisitiongrid.columns[1].show();
                            dataacquisitiongrid.columns[2].show();
                        });
//                        Ext.Object.each(checkColumns, function(id, chkCol, myself) {
//                            chkCol.enable();
//                        });
                        // TODO: Enable action columns
//                        Ext.Object.each(actionColumns, function(id, actionCol, myself) {
//                            actionCol.enable();
//                            actionCol.items[0].disabled = false;
//                            actionCol.enableAction(0);
//                            actionCol.updateLayout();
//                        })
                        btn.setIconCls('fa fa-unlock fa-2x');

                    }
                    else {
                        acq_main[0].columns[3].setWidth(190);
                        acq_main[0].columns[3].setText(' <div class="x-column-header x-column-header-align-left x-box-item x-column-header-default x-unselectable x-column-header-first" style="border-top: 0px; width: 111px; left: 0px; tabindex="-1">' +
                                '           <div data-ref="titleEl" class="x-column-header-inner">' +
                                '               <span data-ref="textEl" class="x-column-header-text">Type</span>' +
                                '           </div>' +
                                '       </div>' +
                                '       <div class="x-column-header x-column-header-align-left x-box-item x-column-header-default x-unselectable" style="border-top: 0px; border-right: 0px; width: 60px; left: 111px; margin: 0px; top: 0px;" tabindex="-1">' +
                                '           <div data-ref="titleEl" class="x-column-header-inner">' +
                                '               <span data-ref="textEl" class="x-column-header-text">Active</span>' +
                                '           </div>' +
                                '       </div>');

                        addproductbtn[0].hide();
                        acq_main[0].columns[0].hide();
                        acq_main[0].columns[2].hide();
                        Ext.Object.each(dataacquisitiongrids, function(id, dataacquisitiongrid, myself) {
                            dataacquisitiongrid.columns[1].hide();
                            dataacquisitiongrid.columns[2].hide();
                        });
//                        Ext.Object.each(checkColumns, function(id, chkCol, myself) {
//                            chkCol.disable();
//                        });
                        // TODO: Disable action columns - problem icon not visible!
//                        Ext.Object.each(actionColumns, function(id, actionCol, myself) {
//                            actionCol.disable();
//                            actionCol.items[0].disabled = true;
//                            actionCol.disableAction(0);
//                            actionCol.updateLayout();
//                        })
                        btn.setIconCls('fa fa-lock fa-2x');
                    }

                    Ext.resumeLayouts(true);
                    // acq_main.updateLayout();

        //                var toggleFn = newValue ? 'disable' : 'enable';
        //                Ext.each(this.query('button'), function(item) {
        //                    item[toggleFn]();
        //                });
                }
            }, {
                xtype: 'button',
                text: 'Add Product',
                name: 'addproduct',
                iconCls: 'fa fa-plus-circle fa-2x',
                style: { color: 'gray' },
                hidden: true,
                // glyph: 'xf055@FontAwesome',
                scale: 'medium',
                handler: 'selectProduct'
            },{
                text: 'Expand All',
                handler: function(btn) {
                    var view = btn.up().up().getView();
                    view.getFeature('productcategories').expandAll();
                    view.refresh();
                }
            }, {
                text: 'Collapse All',
                handler: function(btn) {
                    var view = btn.up().up().getView();
                    view.getFeature('productcategories').collapseAll();
                    view.refresh();
                }
            }, '->', {
                xtype: 'splitbutton',
                name: 'eumetcastbtn',
                text: 'EumetCast',
                iconCls: 'fa fa-cog fa-2x', // fa-spin 'icon-play', // icomoon fonts
                style: { color: 'gray' },
                // glyph: 'xf0c7@FontAwesome',
                scale: 'medium',
                handler: 'checkStatusServices',
                listeners : {
                    render: 'checkStatusServices'
                },
                menu: Ext.create('Ext.menu.Menu', {
                    width: 100,
                    margin: '0 0 10 0',
                    floating: true,  // usually you want this set to True (default)
                    items: [
                        // these will render as dropdown menu items when the arrow is clicked:
                        {   text: 'Run',
                            name: 'runeumetcast',
                            // iconCls: 'fa-play-circle-o', // xf01d   // fa-play xf04b
                            glyph: 'xf04b@FontAwesome',
                            cls:'menu-glyph-color-green',
                            // style: { color: 'green' },
                            handler: 'execServiceTask'
                        },
                        {   text: 'Stop',
                            name: 'stopeumetcast',
                            // iconCls: 'fa fa-stop',
                            glyph: 'xf04d@FontAwesome',
                            cls:'menu-glyph-color-red',
                            // style: { color: 'red' },
                            handler: 'execServiceTask'
                        },
                        {   text: 'Restart',
                            name: 'restarteumetcast',
                            // iconCls: 'fa fa-refresh',
                            glyph: 'xf021@FontAwesome',
                            cls:'menu-glyph-color-orange',
                            // style: { color: 'orange' },
                            handler: 'execServiceTask'
                        }
                    ]
                })
            },
            // add a vertical separator bar between toolbar items
            '-', // same as {xtype: 'tbseparator'} to create Ext.toolbar.Separator
            {
                xtype: 'splitbutton',
                name: 'internetbtn',
                text: 'Internet',
                iconCls: 'fa fa-cog fa-2x',  // 'icon-stop', // icomoon fonts
                style: { color: 'gray' },
                // glyph: 0xf05a,
                scale: 'medium',
                handler: 'checkStatusServices',
                menu: Ext.create('Ext.menu.Menu', {
                    width: 100,
                    margin: '0 0 10 0',
                    floating: true,  // usually you want this set to True (default)
                    items: [
                        // these will render as dropdown menu items when the arrow is clicked:
                        {   text: 'Run',
                            name: 'runinternet',
                            // iconCls: 'fa-play-circle-o', // xf01d   // fa-play xf04b
                            glyph: 'xf04b@FontAwesome',
                            cls:'menu-glyph-color-green',
                            // style: { color: 'green' },
                            handler: 'execServiceTask'
                        },
                        {   text: 'Stop',
                            name: 'stopinternet',
                            // iconCls: 'fa fa-stop',
                            glyph: 'xf04d@FontAwesome',
                            cls:'menu-glyph-color-red',
                            // style: { color: 'red' },
                            handler: 'execServiceTask'
                        },
                        {   text: 'Restart',
                            name: 'restartinternet',
                            // iconCls: 'fa fa-refresh',
                            glyph: 'xf021@FontAwesome',
                            cls:'menu-glyph-color-orange',
                            // style: { color: 'orange' },
                            handler:'execServiceTask'
                        }
                    ]
                })
            }, '-', {
                xtype: 'splitbutton',
                name: 'ingestbtn',
                text: 'Ingest',
                iconCls: 'fa fa-cog fa-2x',  //  fa-spin 'icon-loop', // icomoon fonts
                style: { color: 'gray' },
                // glyph: 'e600@icomoon',
                scale: 'medium',
                handler: 'checkStatusServices',
                menu: Ext.create('Ext.menu.Menu', {
                    width: 100,
                    margin: '0 0 10 0',
                    floating: true,  // usually you want this set to True (default)
                    items: [
                        // these will render as dropdown menu items when the arrow is clicked:
                        {   text: 'Run',
                            name: 'runintgest',
                            // iconCls: 'fa-play-circle-o', // xf01d   // fa-play xf04b
                            glyph: 'xf04b@FontAwesome',
                            cls:'menu-glyph-color-green',
                            // style: { color: 'green' },
                            handler: 'execServiceTask'
                        },
                        {   text: 'Stop',
                            name: 'stopingest',
                            // iconCls: 'fa fa-stop',
                            glyph: 'xf04d@FontAwesome',
                            cls:'menu-glyph-color-red',
                            // style: { color: 'red' },
                            handler: 'execServiceTask'
                        },
                        {   text: 'Restart',
                            name: 'restartingest',
                            // iconCls: 'fa fa-refresh',
                            glyph: 'xf021@FontAwesome',
                            cls:'menu-glyph-color-orange',
                            // style: { color: 'orange' },
                            handler: 'execServiceTask'
                        }
                    ]
                })
            },
            '->', // same as { xtype: 'tbfill' }
            {
                xtype: 'button',
                iconCls: 'fa fa-refresh fa-2x',
                style: { color: 'gray' },
                enableToggle: false,
                scale: 'medium',
                handler:  function(btn) {
                    var productgridstore  = Ext.data.StoreManager.lookup('ProductsActiveStore');
                    var acqgridsstore = Ext.data.StoreManager.lookup('DataAcquisitionsStore');
                    var ingestiongridstore = Ext.data.StoreManager.lookup('IngestionsStore');

                    if (productgridstore.isStore) {
                        productgridstore.load();
                    }
                    if (acqgridsstore.isStore) {
                        acqgridsstore.load();
                    }
                    if (ingestiongridstore.isStore) {
                        ingestiongridstore.load();
                    }
                    // btn.up().up().doLayout();
        //                var view = btn.up().up().getView();
        //                view.getFeature('productcategories').expandAll();
        //                view.refresh();
                }
        //        {
        //            xtype: 'textfield',
        //            width: 300,
        //            hidden:true,
        //            name: 'search_acq',
        //            emptyText: 'enter search term'
        //        }
            // ,'Search' // same as {xtype: 'tbtext', text: 'text1'} to create Ext.toolbar.TextItem
            }]
        });

//        me.listeners = {
//            afterrender: function(gridpanel,func){
//                Ext.toast({ html: 'Afterrender', title: 'Afterrender', width: 200, align: 't' });
//
//                var view = gridpanel.getView();
//                view.getFeature('productcategories').expandAll();
//                view.refresh();
//                // gridpanel.doLayout();
//            }
//        };

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
            // sealed:true,
            defaults: {
                menuDisabled: true,
                variableRowHeight : true,
                sortable: false,
                groupable:true,
                draggable:false,
                hideable: true
            },
            columns: [{
                xtype: 'actioncolumn',
                hideable: true,
                hidden:true,
                width: 30,
                align: 'center',
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
                        '<b>{prod_descriptive_name}</b><br>' +
                        '<span class="smalltext">' +
                        '<b style="color:darkgrey">{productcode}' +
                            '<tpl if="version != \'undefined\'">',
                                ' - {version}',
                            '</tpl>',
                        '</b>' +
                        // '<p>{description}</p>' +
                        '</span><br>'
                    ),
                width: 265,
                cellWrap:true
//                ,hideable: false
            },{
                xtype: 'actioncolumn',
                header: 'Active',
                hideable: true,
                hidden:true,
                width: 65,
                align: 'center',
                shrinkWrap: 0,
                items: [{
                    // scope: me,
                    // handler: me.onToggleActivation
                    getClass: function(v, meta, rec) {
                        if (rec.get('activated')) {
                            return 'activated';
                        } else {
                            return 'deactivated';
                        }
                    },
                    getTip: function(v, meta, rec) {
                        if (rec.get('activated')) {
                            return 'Deactivate Product';
                        } else {
                            return 'Activate Product';
                        }
                    },
                    handler: function(grid, rowIndex, colIndex) {
                        var rec = grid.getStore().getAt(rowIndex),
                            action = (rec.get('activated') ? 'deactivated' : 'activated');
                        Ext.toast({ html: action + ' ' + rec.get('productcode'), title: 'Action', width: 300, align: 't' });
                        rec.get('activated') ? rec.set('activated', false) : rec.set('activated', true);
                    }
                }]
//            }, {
//                xtype: 'checkcolumn',
//                header: 'Active',
//                width: 65,
//                dataIndex: 'activated',
//                stopSelection: false,
//                hideable: true,
//                hidden:true,
//                disabled: true,
//                listeners: {
//                  checkchange: function(chkBox, rowIndex, checked, eOpts){
////                      var myTitle = ""
////                      if (checked)  myTitle = "Activate Product";
////                      else myTitle = "De-activate Product";
////                      Ext.toast({ html: 'Checkbox clicked!', title: myTitle, width: 200, align: 't' });
//                  }
//                }
    //            xtype: 'booleancolumn',
    //            header: 'Active',
    //            width: 80,
    //            sortable: true,
    //            dataIndex: 'activated',
    //            stopSelection: false,
    //            trueText: '&#x2713;',
    //            falseText: '-',
    //            align: 'center'
            }]
        }, {
            header:  '<div class="grid-header-style">Acquisition</div>',
            id:'acquisitioncolumn',
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
                xtype: 'widgetcolumn',
                width: 190,

                header: ' <div class="x-column-header x-column-header-align-left x-box-item x-column-header-default x-unselectable x-column-header-first" style="border-top: 0px; width: 111px; left: 0px; tabindex="-1">' +
                '           <div data-ref="titleEl" class="x-column-header-inner">' +
                '               <span data-ref="textEl" class="x-column-header-text">Type</span>' +
                '           </div>' +
                '       </div>' +
                '       <div class="x-column-header x-column-header-align-left x-box-item x-column-header-default x-unselectable" style="border-top: 0px; border-right: 0px; width: 60px; left: 111px; margin: 0px; top: 0px;" tabindex="-1">' +
                '           <div data-ref="titleEl" class="x-column-header-inner">' +
                '               <span data-ref="textEl" class="x-column-header-text">Active</span>' +
                '           </div>' +
                '       </div>',

//                header: ' <div class="x-column-header x-column-header-align-left x-box-item x-column-header-default x-unselectable x-column-header-first" style="border-top: 0px; width: 111px; left: 0px; tabindex="-1">' +
//                '           <div data-ref="titleEl" class="x-column-header-inner">' +
//                '               <span data-ref="textEl" class="x-column-header-text">Type</span>' +
//                '           </div>' +
//                '       </div>' +
//                '       <div class="x-column-header x-column-header-align-left x-box-item x-column-header-default x-unselectable" style="border-top: 0px; width: 110px; right: auto; left: 111px; margin: 0px; top: 0px;" tabindex="-1">' +
//                '           <div data-ref="titleEl" class="x-column-header-inner">' +
//                '               <span data-ref="textEl" class="x-column-header-text">Last copied</span>' +
//                '           </div>' +
//                '       </div>' +
//                '       <div class="x-column-header x-column-header-align-left x-box-item x-column-header-default x-unselectable" style="border-top: 0px; width: 110px; right: auto; left: 221px; margin: 0px; top: 0px;" tabindex="-1">' +
//                '           <div data-ref="titleEl" class="x-column-header-inner">' +
//                '               <span data-ref="textEl" class="x-column-header-text">Last executed</span>' +
//                '           </div>' +
//                '       </div>' +
//                '       <div class="x-column-header x-column-header-align-left x-box-item x-column-header-default x-unselectable" style="border-top: 0px; border-right: 0px; width: 60px; left: 332px; margin: 0px; top: 0px;" tabindex="-1">' +
//                '           <div data-ref="titleEl" class="x-column-header-inner">' +
//                '               <span data-ref="textEl" class="x-column-header-text">Active</span>' +
//                '           </div>' +
//                '       </div>',

                listeners: {
                    render: function(column){
                        column.titleEl.removeCls('x-column-header-inner');
                    }
                },
                onWidgetAttach: function(widget, record) {
                    Ext.suspendLayouts();

                    var daStore = widget.getViewModel().get('productdatasources');
                    daStore.setFilters({
                         property:'productID'
                        ,value:record.id
                        ,anyMatch:true
                    });

                     Ext.resumeLayouts(true);
                },
                widget: {
                    xtype: 'dataacquisitiongrid'
                }
            }]
        }, {
            header:  '<div class="grid-header-style">Ingestion</div>',
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
                width: 780,
                bodyPadding:0,

                header: ' <div class="x-column-header  x-column-header-align-left x-box-item x-column-header-default x-unselectable" style="border-top: 0px; width: 170px; left: 0px; tabindex="-1">' +
                '           <div data-ref="titleEl" class="x-column-header-inner">' +
                '               <span data-ref="textEl" class="x-column-header-text">Mapset</span>' +
                '           </div>' +
                '       </div>' +
                '       <div class="x-column-header x-column-header-align-left x-box-item x-column-header-default x-unselectable" style="border-top: 0px; width: 100px; right: auto; left: 170px; margin: 0px; top: 0px;" tabindex="-1">' +
                '           <div data-ref="titleEl" class="x-column-header-inner">' +
                '               <span data-ref="textEl" class="x-column-header-text">Sub Product</span>' +
                '           </div>' +
                '       </div>' +
                '       <div class="x-column-header x-column-header-align-left x-box-item x-column-header-default x-unselectable" style="border-top: 0px; width: 360px; right: auto; left: 270px; margin: 0px; top: 0px;" tabindex="-1">' +
                '           <div data-ref="titleEl" class="x-column-header-inner">' +
                '               <span data-ref="textEl" class="x-column-header-text">Completeness</span>' +
                '           </div>' +
                '       </div>' +
                '       <div class="x-column-header x-column-header-align-left x-box-item x-column-header-default x-unselectable" style="border-top: 0px; width: 65px; right: auto; left: 630px; margin: 0px; top: 0px;" tabindex="-1">' +
                '           <div data-ref="titleEl" class="x-column-header-inner">' +
                '               <span data-ref="textEl" class="x-column-header-text">Active</span>' +
                '           </div>' +
                '       </div>' +
                '       <div class="x-column-header x-column-header-align-left x-box-item x-column-header-default x-unselectable" style="border-top: 0px; border-right: 0px; width: 70px;  left: 695px; margin: 0px; top: 0px;" tabindex="-1">' +
                '           <div data-ref="titleEl" class="x-column-header-inner">' +
                '               <span data-ref="textEl" class="x-column-header-text">Actions</span>' +
                '           </div>' +
                '       </div>',
                listeners: {
                  render: function(column){
                      column.titleEl.removeCls('x-column-header-inner');
                      // column.doLayout();
                  }
                },
                onWidgetAttach: function(widget, record) {
                    // Ext.suspendLayouts();

                    // widget.setVisible(record.get('score') > 50);
                    var daStore = widget.getViewModel().get('productingestions');
                    daStore.setFilters({
                         property:'productID'
                        ,value:record.id
                        ,anyMatch:true
                    });
                    // Ext.resumeLayouts(true);
                },
                widget: {
                    xtype: 'ingestiongrid'
                }
            }]
        }];

        me.callParent();
    }
});