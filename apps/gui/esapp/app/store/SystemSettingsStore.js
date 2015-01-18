Ext.define('esapp.store.SystemSettingsStore', {
     extend  : 'Ext.data.Store'
    ,alias: 'store.systemsettings'

    ,requires : [
        'esapp.model.SystemSetting',
        'Ext.data.proxy.Rest'
    ]
    ,model: 'esapp.model.SystemSetting'

    ,storeId : 'SystemSettingsStore'

});
