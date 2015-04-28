Ext.define('esapp.view.analysis.analysisMainModel', {
    extend: 'Ext.app.ViewModel',
    alias: 'viewmodel.analysis-analysismain',

    stores: {
        products: {
            model: 'esapp.model.TimeseriesProduct'
            ,session: true
            ,autoLoad:false
            ,loadMask: true

            ,sorters: {property: 'order_index', direction: 'DESC'}

            ,grouper:{
                     // property: 'cat_descr_name',
                     groupFn : function (item) {
                         return "<span style='display: none;'>" + item.get('order_index') + "</span>" + item.get('cat_descr_name')
                         //return item.get('cat_descr_name')
                     },
                     sortProperty: 'order_index'
            }
            ,listeners: {
                write: function(store, operation){
                    Ext.toast({ html: operation.getResultSet().message, title: operation.action, width: 300, align: 't' });
                }
            }
        },
        productmapsets: {
            model: 'esapp.model.TimeserieProductMapSet'
            ,session: true
        },
        timeseriesmapsetdatasets:{
            model: 'esapp.model.TimeserieProductMapSetDataSet'
            ,session: true
        },
        years:{
            //model: 'esapp.model.Year'
            fields: ['year'],
            data: [
                {year: 2010},
                {year: 2011},
                {year: 2012},
                {year: 2013},
                {year: 2014},
                {year: 2015}
                //[2010],
                //[2011],
                //[2012],
                //[2013],
                //[2014],
                //[2015]
            ]
        }
    }

});
