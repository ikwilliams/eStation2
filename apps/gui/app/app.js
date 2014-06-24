
Ext.application({
    name: 'AM',

	// automatically create an instance of AM.view.Viewport
//	requires: ['Ext.container.Viewport'],
	autoCreateViewport: true,

    appFolder: 'app',

	controllers: [
	     'Users'
	]

//    ,launch: function() {
//        Ext.create('Ext.container.Viewport', {
//            layout: 'fit',
//            items: [
//                {
//                    xtype: 'panel',
//                    title: 'Users',
//                    html : 'List of users will go here'
//                }
//            ]
//        });
//    }
});