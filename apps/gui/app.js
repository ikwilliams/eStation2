Ext.Loader.setConfig({enabled: true});

Ext.Loader.setPath('Ext.ux', '../../../lib/js/Ext.ux');

Ext.require([
    'Ext.grid.*',
    'Ext.data.*',
    'Ext.util.*',
    'Ext.tip.QuickTipManager',
    'Ext.ux.LiveSearchGridPanel',
	'Ext.toolbar.Toolbar',
	'Ext.menu.ColorPicker',
	'Ext.form.field.Date'
]);

Ext.onReady(function() {
    Ext.QuickTips.init();


    /**
     * Custom function used for column renderer
     * @param {Object} val
     */
    function change(val){
        if(val > 0){
            return '<span style="color:green;">' + val + '</span>';
        }else if(val < 0){
            return '<span style="color:red;">' + val + '</span>';
        }
        return val;
    }

    /**
     * Custom function used for column renderer
     * @param {Object} val
     */
    function pctChange(val){
        if(val > 0){
            return '<span style="color:green;">' + val + '%</span>';
        }else if(val < 0){
            return '<span style="color:red;">' + val + '%</span>';
        }
        return val;
    }

	var handleAction = function(action){
		Ext.example.msg('<b>Action</b>', 'You clicked "' + action + '"');
	};

	var colorMenu = Ext.create('Ext.menu.ColorPicker', {
		handler: function(cm, color){
			Ext.example.msg('Color Selected', '<span style="color:#' + color + ';">You choose {0}.</span>', color);
		}
	});


	var acq_tbar = Ext.create('Ext.toolbar.Toolbar', {
        layout: {
            overflowHandler: 'Menu'
        },
        style: {
            backgroundcolor: '95%'
        },
        items: [{
            xtype:'splitbutton',
            text: 'Menu',
            iconCls: 'add16',
            handler: Ext.Function.pass(handleAction, 'Menu'),
            menu: [{text: 'Menu Item 1', handler: Ext.Function.pass(handleAction, 'Menu Item 1')}]
        },'-',{
            text: 'Click me',
            iconCls: 'add16',
            handler: Ext.Function.pass(handleAction, 'Click me')
        },'->', {
            text: 'Choose a Color',
            menu: colorMenu // <-- submenu by reference
        }]
    });

    // NOTE: This is an example showing simple state management. During development,
    // it is generally best to disable state management as dynamically-generated ids
    // can change across page loads, leading to unpredictable results.  The developer
    // should ensure that stable state ids are set for stateful components in real apps.
//    Ext.state.Manager.setProvider(Ext.create('Ext.state.CookieProvider'));

    Ext.create('Ext.Viewport', {
        id: 'estation2viewport',
        layout: 'border',
        items: [
        // create instance immediately
        Ext.create('Ext.Component', {
            region: 'north',
	        title:'',
            height: 63, // give north and south regions a height
	        contentEl:'north',
	        split: false,
	        collapsible: false,
            collapsed: false
        }), {
            // lazily created panel (xtype:'panel' is default)
            region: 'south',
            contentEl: 'south',
            split: true,
            height: 100,
            minSize: 100,
            maxSize: 200,
            collapsible: true,
            collapsed: true,
            margins: '0 0 0 0'
        }, {
            xtype: 'tabpanel',
            region: 'east',
            dockedItems: [{
                dock: 'top',
                xtype: 'toolbar',
                items: [ '->', {
                   xtype: 'button',
                   text: 'test',
                   tooltip: 'Test Button'
                }]
            }],
            animCollapse: true,
            collapsible: true,
            collapsed: true,
            split: true,
            width: 225, // give east and west regions a width
            minSize: 175,
            maxSize: 400,
            margins: '0 5 0 0',
            activeTab: 1,
            tabPosition: 'bottom',
            items: [{
                html: '<p>A TabPanel component can be a region.</p>',
                title: 'A Tab',
                autoScroll: true
            }, Ext.create('Ext.grid.PropertyGrid', {
                    title: 'Property Grid',
                    closable: true,
                    source: {
                        "(name)": "Properties Grid",
                        "grouping": false,
                        "autoFitColumns": true,
                        "productionQuality": false,
                        "created": Ext.Date.parse('10/15/2006', 'm/d/Y'),
                        "tested": false,
                        "version": 0.01,
                        "borderWidth": 1
                    }
                })]
        }, {
            region: 'west',
            stateId: 'navigation-panel',
            id: 'west-panel', // see Ext.getCmp() below
//            title: 'West',
            split: true,
            width: 200,
            minWidth: 175,
            maxWidth: 400,
            collapsible: true,
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
        },
        // in this instance the TabPanel is not wrapped by another panel
        // since no title is needed, this Panel is added directly
        // as a Container
        Ext.create('Ext.tab.Panel', {
            region: 'center', // a center region is ALWAYS required for border layout
	        layout: 'fit',
            deferredRender: false,
            activeTab: 0,     // first tab initially active
//            tbar: acq_tbar,
//            dockedItems: [{
//                dock: 'top',
//                xtype: 'toolbar',
//                items: [ '->', acq_tbar]
//            }],
            items: [{
                title: 'Acquisition',
                closable: false,
                autoScroll: true,
	            items: []
            }, {
                contentEl: '',
                title: 'Processing',
                autoScroll: true
            }, {
                contentEl: '',
                title: 'Data Management',
                autoScroll: true
            }, {
                contentEl: '',
                title: 'Analysis',
                autoScroll: true
            }, {
                contentEl: '',
                title: 'System',
                autoScroll: true
            }, {
                contentEl: 'center2',
                title: 'Help',
                autoScroll: true
            }],
            listeners: {
                afterrender: function(panel) {
                    var bar = panel.tabBar;
                    bar.insert(6, [{
                        xtype: 'component',
                        flex: 1
                    }, acq_tbar,
                    {
                        xtype: 'button',
                        text: 'button',
                        handler: function() {
                            alert('You have clicked the button!');
                        }
                    }
                    ]);
                }
            }
        })]
    });


    // get a reference to the HTML element with id "hideit" and add a click listener to it
    Ext.get("hideit").on('click', function(){
        // get a reference to the Panel that was created with id = 'west-panel'
        var w = Ext.getCmp('west-panel');
        // expand or collapse that Panel based on its collapsed property state
        w.collapsed ? w.expand() : w.collapse();
    });

});