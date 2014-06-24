Ext.data.dynamicScriptTagProxy = function(conn){
    Ext.data.ScriptTagProxy.superclass.constructor.call(this, conn);
    this.conn = conn;
    this.conn.url = null;
};


Ext.extend(Ext.data.dynamicScriptTagProxy, Ext.data.ScriptTagProxy, {

/**
     * Used for overriding the url used for a single request.  Designed to be called during a beforeaction event.  Calling setUrl
     * will override any urls set via the api configuration parameter.  Set the optional parameter makePermanent to set the url for
     * all subsequent requests.  If not set to makePermanent, the next request will use the same url or api configuration defined
     * in the initial proxy configuration.
     * @param {String} url
     * @param {Boolean} makePermanent (Optional) [false]
     *
     * (e.g.: beforeload, beforesave, etc).
     */
	constructor: function() {
		var api = {};
		api[Ext.data.Api.actions.read] = true;
		Ext.data.ScriptTagProxy.superclass.constructor.call(this, {
			api: api
		});
	},	
	
    setUrl : function(url) {
//        this.api[Ext.data.Api.actions.read] = true;
    	this.conn.url = url;
        this.url = url;
        this.api = null;
        Ext.data.Api.prepare(this);
    }

});