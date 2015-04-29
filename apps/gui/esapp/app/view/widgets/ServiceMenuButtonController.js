Ext.define('esapp.view.widgets.ServiceMenuButtonController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.widgets-servicemenubutton',

    execServiceTask: function(menuitem, ev){
        var me = this;

        // AJAX call to run/start a specified service (specified through the menuitem name).
        // Ext.Ajax.extraParams = {task: menuitem.name};
        Ext.Ajax.request({
            method: 'POST',
            url: 'services/execservicetask',
            // extraParams: {task: menuitem.name},
            params: {
                service: menuitem.service,
                task: menuitem.task
            },
            success: function(response, opts){
                var runresult = Ext.JSON.decode(response.responseText);
                if (runresult.success){
                    //Ext.toast({ html: 'Execute Service ' + menuitem.service + ' is ' + menuitem.task + 'ed', title: 'Service Task Executed', width: 200, align: 't' });
                    // menuitem.up().up().fireEvent('click', this);
                    menuitem.up().up().up().up().getController().checkStatusServices(menuitem.up().up());
                }
            },
            failure: function(response, opts) {
                console.info(response.status);
            }
        });
    }

});
