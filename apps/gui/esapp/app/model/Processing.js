Ext.define('esapp.model.Processing', {
    extend : 'esapp.model.Base',

//    idProperty : 'productID',
    fields: [
       {name: 'productID', type: 'string', mapping: 'productID'},
       {name: 'productcode', mapping: 'productcode'},
       {name: 'subproductcode', mapping: 'subproductcode'}, // Native
       {name: 'version', mapping: 'version'},
       {name: 'defined_by', mapping: 'defined_by'},
       {name: 'product_type', mapping: 'product_type'},
       {name: 'activated', type: 'boolean', mapping: 'activated'},
       {name: 'prod_descriptive_name', mapping: 'prod_descriptive_name'},
       {name: 'description', mapping: 'description'},
       {name: 'category_id', mapping: 'category_id'},
       {name: 'cat_descr_name', mapping: 'cat_descr_name'},
       {name: 'order_index', mapping: 'order_index'}
    ]
});


Ext.define('esapp.model.ProcessingProductMapSet', {
    extend : 'esapp.model.Base',

    fields: [
        {name: 'productID', reference:'Processing', type: 'string'},
        {name: 'mapsetcode'},
        {name: 'defined_by'},
        {name: 'descriptive_name'},
        {name: 'description'},
        {name: 'srs_wkt'},
        {name: 'upper_left_long'},
        {name: 'pixel_shift_long'},
        {name: 'rotation_factor_long'},
        {name: 'upper_left_lat'},
        {name: 'pixel_shift_lat'},
        {name: 'rotation_factor_lat'},
        {name: 'pixel_size_x'},
        {name: 'pixel_size_y'},
        {name: 'footprint_image'}
    ]
});


Ext.define('esapp.model.MapSetFinalOutputSubProducts', {
    extend : 'esapp.model.Base',
//    extend: 'Ext.data.Model',

    fields: [
       {name: 'mapsetcode', reference:'ProcessingProductMapSet'},
       {name: 'datasetID'},
       {name: 'productcode'},
       {name: 'subproductcode'},
       {name: 'version'},
       {name: 'defined_by'},
       {name: 'activated', type: 'boolean'},
       {name: 'product_type'},
       {name: 'prod_descriptive_name'},
       {name: 'description'}
    ]
});

