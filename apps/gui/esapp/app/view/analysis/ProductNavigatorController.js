Ext.define('esapp.view.analysis.ProductNavigatorController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.analysis-productnavigator',

    productsGridAfterrender: function() {
        this.getStore('products').load();
    },

    productsGridRowClick: function(gridview, record){
        console.info(record);
        //var productinfopanel = Ext.ComponentQuery.query('panel[id=ProductDataSetsInfo]')[0];
        var productinfopanel = gridview.up().up().down('panel[id=ProductDataSetsInfo]');
        productinfopanel.setTitle('<div class="panel-title-style">Product: ' + record.data.prod_descriptive_name + '</div>');
        productinfopanel.expand(true);
    }
});
