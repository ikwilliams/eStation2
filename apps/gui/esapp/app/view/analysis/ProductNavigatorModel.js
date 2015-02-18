Ext.define('esapp.view.analysis.ProductNavigatorModel', {
    extend: 'Ext.app.ViewModel',
    alias: 'viewmodel.analysis-productnavigator',

    //data : {
    //    ProductNavigator : {},
    //    ProductNavigatorMapSet : {},
    //    ProductNavigatorMapSetDataSet : {}
    //}

    stores: {
        products: {
            //model: 'ProductNavigator'
            source: 'ProductNavigatorStore'
            //,autoload: true
            //,grouper:{
            //         // property: 'cat_descr_name',
            //         groupFn : function (item) {
            //             return "<span style='display: none;'>" + item.get('order_index') + "</span>" + item.get('cat_descr_name')
            //             //return item.get('cat_descr_name')
            //         },
            //         sortProperty: 'order_index'
            //}
        }
    }

});
