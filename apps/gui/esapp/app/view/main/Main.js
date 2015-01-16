/**
 * This class is the main view for the application. It is specified in app.js as the
 * "autoCreateViewport" property. That setting automatically applies the "viewport"
 * plugin to promote that instance of this class to the body element.
 */

Ext.define('esapp.view.main.Main', {
    extend: 'Ext.container.Container',

    xtype: 'app-main',
    requires: [
        'Ext.layout.container.Center'
        //,'Ext.chart.CartesianChart'
    ],
    controller: 'main',
    viewModel: {
        type: 'main'
    },

    layout: {
        type: 'border'
    },
    ptype:'lazyitems',
    items: [{
            region: 'north',
            id: 'headerlogos',
            xtype:'container',
	        title:'',
            height: 63,
            items:[{
                xtype : 'headerLogos'
            }],
	        split: false,
	        collapsible: false,
            collapsed: false
        },{
            region: 'west',
            stateId: 'navigation-panel',
            id: 'west-panel', // see Ext.getCmp() below
            title: '',
            split: true,
            width: 200,
            collapsible: true,
            collapsed: true,
            animCollapse: true,
            margins: '0 0 0 5',
            layout: 'accordion',
            items: [{
                contentEl: 'west',
                title: 'Navigation',
                iconCls: 'nav' // see the HEAD section for style used
            }, {
                title: 'Settings',
                html: '<p>Some settings in here.</p>',
                iconCls: 'settings'
            }, {
                title: 'Information',
                html: '<p>Some info in here.</p>',
                iconCls: 'info'
            }]
        },{
            region: 'center',
            xtype: 'tabpanel',
            layout: 'fit',
            deferredRender: false,
            activeTab: 'dashboardtab',     // first tab initially active

//            tbar: { xtype: 'app-main-toolbar' },
//            dockedItems: [{
//                dock: 'top',
//                xtype: 'toolbar',
//                items: [ '->', acq_tbar]
//            }],

            items: [{
                title: 'Dashboard',
                id:'dashboardtab',
                xtype:'container',
                autoScroll: true,
                layout : 'center',
                bodyCls:'dashboard-panel-body',
	            items: [{
                    xtype: 'dashboard-main'
                }],
                listeners: {
                   activate: function (analisistab) {
                        var headerlogos = Ext.ComponentQuery.query('container[id=headerlogos]')[0];
                        headerlogos.setHidden(false);
                   }
                }
            }, {
                title: 'Acquisition',
                id:'acquisitionmaintab',
                xtype:'container',
                closable: false,
                autoScroll: true,
                layout: 'fit',
	            items: [{
                    // html: '<img alt="Mockup Acquisition" width="100%" height="100%" src="../resources/img/mockup_acquisition.png">'
                    xtype : 'acquisition-main',
                    id:'acquisitionmain'
                }],
                listeners: {
                   activate: function () {
                        var headerlogos = Ext.ComponentQuery.query('container[id=headerlogos]')[0];
                        headerlogos.setHidden(false);
////                       console.info(this.down('toolbar > button[name=eumetcastbtn]'));
//                       var eumetcastbtn = this.down('toolbar > button[name=eumetcastbtn]');
//                       eumetcastbtn.fireEvent('render', eumetcastbtn.scope);
                   }
                }
            }, {
                title: 'Processing',
                id:'processingmaintab',
                xtype:'container',
                autoScroll: true,
                layout: 'fit',
	            items: [{
                   xtype  : 'processing-main',
                   id:'processingmain'
                }],
                listeners: {
                   activate: function (analisistab) {
                        var headerlogos = Ext.ComponentQuery.query('container[id=headerlogos]')[0];
                        headerlogos.setHidden(false);
                   }
                }
            }, {
                title: 'Data Management',
                id:'datamanagementmaintab',
                xtype:'container',
                autoScroll: true,
                layout: 'fit',
	            items: [{
                   xtype  : 'datamanagement-main',
                   id:'datamanagementmain'
                }],
                listeners: {
                   activate: function (analisistab) {
                        var headerlogos = Ext.ComponentQuery.query('container[id=headerlogos]')[0];
                        headerlogos.setHidden(false);
                   }
                }
            }, {
                title: 'Analysis',
                id:'analysistab',
                xtype:'container',
                autoScroll: true,
                layout : 'fit',
	            items: [{
                   xtype  : 'analysis-main',
                   id:'analysismain'
                }],
                listeners: {
                   activate: function (analisistab) {
                        var headerlogos = Ext.ComponentQuery.query('container[id=headerlogos]')[0];
                        headerlogos.setHidden(true);
                   }
                }
            }, {
                title: 'System',
                xtype:'container',
                autoScroll: true,
                layout : 'center',
	            items: [{
                   xtype  : 'systemsettings',
                   id:'systemsettings'
                }],
                listeners: {
                   activate: function (analisistab) {
                        var headerlogos = Ext.ComponentQuery.query('container[id=headerlogos]')[0];
                        headerlogos.setHidden(false);
                   }
                }
            }, {
                title: 'Help',
                xtype:'container',
                autoScroll: true,
                html: '', // '<a id="hideit" href="#">Toggle the west region</a>',
                listeners: {
                   activate: function (analisistab) {
                        var headerlogos = Ext.ComponentQuery.query('container[id=headerlogos]')[0];
                        headerlogos.setHidden(false);
                   }
                }
            }]

        }]
});