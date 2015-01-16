Ext.define('esapp.store.SystemSettingsStore', {
     extend  : 'Ext.data.Store'
    ,alias: 'store.systemsettings'

    ,requires : [
        'esapp.model.SystemSetting',
        'Ext.data.proxy.Rest'
    ]
    ,model: 'esapp.model.SystemSetting'

    ,storeId : 'SystemSettingsStore'

//    ,autoLoad: true
//    ,autoSync: true
//    ,remoteSort: false
//    ,remoteGroup: false

//    ,proxy: {
//        type: 'rest',
//
//        appendId: false,
//        extraParams:{
//            activated:'True'
//        },
//        api: {
//            read: 'systemsettings',
//            create: 'systemsettings/create',
//            update: 'systemsettings/update',
//            destroy: 'systemsettings/delete'
//        },
//        reader: {
//             type: 'json'
//            ,successProperty: 'success'
//            ,rootProperty: 'systemsettings'
//            ,messageProperty: 'message'
//        },
//        writer: {
//            type: 'json',
//            writeAllFields: true,
//            rootProperty: 'systemsettings'
//        },
//        listeners: {
//            exception: function(proxy, response, operation){
//                Ext.MessageBox.show({
//                    title: 'SYSTEM SETTINGS STORE - REMOTE EXCEPTION',
//                    msg: operation.getError(),
//                    icon: Ext.MessageBox.ERROR,
//                    buttons: Ext.Msg.OK
//                });
//            }
//        }
//    }

    ,listeners: {
        update: function(store, record, operation, modifiedFieldNames, details, eOpts  ){

        },
        write: function(store, operation){
            if (operation.action == 'update' && operation.success) {
                var records = operation.getRecords();
                store.suspendAutoSync();
                store.remove(records[0], true);
                store.resumeAutoSync();
            }
//            if (operation.action == 'destroy') {
//                // main.child('#form').setActiveRecord(null);
//            }
//            Ext.toast({ html: operation.getResultSet().message, title: operation.action, width: 200, align: 't' });
        }
    }

});
