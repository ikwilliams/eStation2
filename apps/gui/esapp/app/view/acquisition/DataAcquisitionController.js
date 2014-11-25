Ext.define('esapp.view.acquisition.DataAcquisitionController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.dataacquisition',

    requires: [
        'Ext.window.Toast'
    ],

    onRemoveClick: function(grid, rowIndex){
//        grid.getStore().removeAt(rowIndex);
        Ext.toast({
            html: 'Removed row!',
            title: 'onRemoveClick',
            width: 200,
            align: 't'
        });
    }
});
