Ext.define('esapp.view.analysis.ProductNavigatorController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.analysis-productnavigator',

    loadProductsStore: function() {

        var prodgrid = this.getView().lookupReference('productsGrid');
        var myLoadMask = new Ext.LoadMask({
            msg    : 'Loading...',
            target : prodgrid
        });
        myLoadMask.show();

        this.getStore('products').load({
            callback:function(){
                myLoadMask.hide();
            }
        });
    },

    refreshProductsGrid: function() {

        var productinfopanel = this.getView().lookupReference('product-datasets-info');
        productinfopanel.setTitle('<div class="panel-title-style-16">Product Info</div>');
        productinfopanel.collapse();

        var mapsetdatasetgrid = this.getView().lookupReference('mapset-dataset-grid');
        if (mapsetdatasetgrid){
            mapsetdatasetgrid.hide();
        }

        this.getStore('mapsetdatasets').removeAll();
        this.getStore('productmapsets').removeAll();

        var prodgrid = this.getView().lookupReference('productsGrid');
        var myLoadMask = new Ext.LoadMask({
            msg    : 'Loading...',
            target : prodgrid
        });
        myLoadMask.show();

        this.getStore('products').load({
            callback:function(){
                myLoadMask.hide();
            }
        });
        //    var productsgridstore  = Ext.data.StoreManager.lookup('ProductNavigatorStore');
        //    var productsgridstore = productnavwin.lookupReference('productsGrid').getStore('products');
        //    if (productsgridstore.isStore) {
        //        productsgridstore.load({loadMask:true});
        //    }
    },

    productsGridRowClick: function(gridview, record){

        this.lookupReference('mapset-dataset-grid').hide();
        this.getStore('mapsetdatasets').removeAll();
        this.getStore('productmapsets').removeAll();
        this.getStore('productmapsets').setData(record.get('productmapsets'));

        //var mapsets = record.data.productmapsets;
        //var itemsInGroup = [];
        //
        //for (var i = 0, l = mapsets.length; i < l; i++) {
        //    var mapset = mapsets[i];
        //
        //    itemsInGroup.push( {
        //        boxLabel: mapset.descriptive_name,
        //        name: mapset.mapsetcode,
        //        inputValue: mapset.mapsetcode
        //    });
        //}
        //
        //var myGroup = {
        //  xtype: 'radiogroup',
        //  fieldLabel: '',
        //  items: itemsInGroup
        //};
        //
        //var productinfopanel = Ext.ComponentQuery.query('panel[id=product-datasets-info]')[0];
        //var productinfopanel = gridview.up().up().down('panel[reference=product-datasets-info]');
        //productinfopanel.down('fieldset').removeAll();
        //productinfopanel.down('fieldset').add(myGroup);
        var productinfopanel = this.lookupReference('product-datasets-info');
        productinfopanel.setTitle('<div class="panel-title-style-16">' + record.get('prod_descriptive_name') + '</div>');
        productinfopanel.expand(true);
    },

    mapsetItemClick: function(dataview, record ){
        // nodes contain all selected records when dataview has multiSelect to true!
        // here we do not use multiSelect so nodes is the record of the selected mapset!
        this.getStore('mapsetdatasets').setData(record.get('mapsetdatasets'));
        var mapsetdatasetgrid = this.lookupReference('mapset-dataset-grid');
        mapsetdatasetgrid.columns[0].setText('<span class="grid-header-style">Data sets</span>' + ' for mapset ' + record.get('descriptive_name'));
        mapsetdatasetgrid.doLayout();
        mapsetdatasetgrid.show();
    }
});
