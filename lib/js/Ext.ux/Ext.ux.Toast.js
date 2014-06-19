/* add the changecomplete event to the sliderfield
*/
Ext.sequence( Ext.form.SliderField.prototype, 'initComponent', function() {
	this.slider.on( 'change', this.fireEvent.createDelegate( this, 'change', 0 ) );
	this.slider.on( 'changecomplete', this.fireEvent.createDelegate( this, 'changecomplete', 0 ) );
});


Ext.namespace("Ext.ux");
//parseUri 1.2.2
//(c) Steven Levithan <stevenlevithan.com>
//MIT License

Ext.ux.parseUri = function (str) {
	var	o   = Ext.ux.parseUri.options,
		m   = o.parser[o.strictMode ? "strict" : "loose"].exec(str),
		uri = {},
		i   = 14;

	while (i--) uri[o.key[i]] = m[i] || "";

	uri[o.q.name] = {};
	uri[o.key[12]].replace(o.q.parser, function ($0, $1, $2) {
		if ($1) uri[o.q.name][$1] = $2;
	});

	return uri;
};

Ext.ux.parseUri.options = {
	strictMode: false,
	key: ["source","protocol","authority","userInfo","user","password","host","port","relative","path","directory","file","query","anchor"],
	q:   {
		name:   "queryKey",
		parser: /(?:^|&)([^&=]*)=?([^&]*)/g
	},
	parser: {
		strict: /^(?:([^:\/?#]+):)?(?:\/\/((?:(([^:@]*)(?::([^:@]*))?)?@)?([^:\/?#]*)(?::(\d*))?))?((((?:[^?#\/]*\/)*)([^?#]*))(?:\?([^#]*))?(?:#(.*))?)/,
		loose:  /^(?:(?![^:@]+:[^:@\/]*@)([^:\/?#.]+):)?(?:\/\/)?((?:(([^:@]*)(?::([^:@]*))?)?@)?([^:\/?#]*)(?::(\d*))?)(((\/(?:[^?#](?![^?#\/]*\.[^?#\/.]+(?:[?#]|$)))*\/?)?([^?#\/]*))(?:\?([^#]*))?(?:#(.*))?)/
	}
};


/**
 * @class Ext.ux.Toast
 * Passive popup box (a toast) singleton
 * @singleton
 */
Ext.ux.Toast = function() {
    var msgCt;

    function createBox(t, s){
        return ['<div class="msg">',
                '<div class="x-box-tl"><div class="x-box-tr"><div class="x-box-tc"></div></div></div>',
                '<div class="x-box-ml"><div class="x-box-mr"><div class="x-box-mc"><h3>', t, '</h3>', s, '</div></div></div>',
                '<div class="x-box-bl"><div class="x-box-br"><div class="x-box-bc"></div></div></div>',
                '</div>'].join('');
    }

    return {
		/**
		 * Shows popup
		 * @member Ext.ux.Toast
		 * @param {String} title
		 * @param {String} format
		 */
        msg : function(title, format){
            if(!msgCt){
                msgCt = Ext.DomHelper.insertFirst(document.body, {id:'msg-div',style:'position:absolute;z-index:10000'}, true);
            }
            var s = String.format.apply(String, Array.prototype.slice.call(arguments, 1));
            var m = Ext.DomHelper.append(msgCt, {html:createBox(title, s)}, true);
            msgCt.alignTo(document, 't-t');
            m.slideIn('t').pause(3.5).ghost("t", {remove:true});
        }
	}

}();


Ext.ux.NotificationMgr = {
		notifications: [],
		originalBodyOverflowY: null
};

Ext.ux.Notification = Ext.extend(Ext.Window, {
    initComponent: function(){
        Ext.apply(this, {
            iconCls: this.iconCls || 'x-icon-information',
            cls: 'x-notification',
            width: 200,
            autoHeight: true,
            plain: true,
            header: false,
        	border: false,
        	closable: false,
        	draggable: false,
            bodyStyle: 'text-align:left'
        });
        if(this.autoDestroy) {
            this.task = new Ext.util.DelayedTask(this.hide, this);
        } else {
            this.closable = true;
        }
        Ext.ux.Notification.superclass.initComponent.apply(this);
    },
    setMessage: function(msg){
        this.body.update(msg);
    },
    setTitle: function(title, iconCls){
        Ext.ux.Notification.superclass.setTitle.call(this, title, iconCls||this.iconCls);
    },
    onDestroy: function(){
        Ext.ux.NotificationMgr.notifications.remove(this);
        Ext.ux.Notification.superclass.onDestroy.call(this);   
    },
    cancelHiding: function(){
        this.addClass('fixed');
        if(this.autoDestroy) {
            this.task.cancel();
        }
    },
    afterShow: function(){
        Ext.ux.Notification.superclass.afterShow.call(this);
        Ext.fly(this.body.dom).on('click', this.cancelHiding, this);
        if(this.autoDestroy) {
            this.task.delay(this.hideDelay || 50000);
       }
    },
    animShow: function() {
		// save original body overflowY
		if (Ext.ux.NotificationMgr.originalBodyOverflowY == null)
		{
			Ext.ux.NotificationMgr.originalBodyOverflowY = document.body.style.overflowY;
		}

		// if the body haven't horizontal scrollbar it should not appear
		if (document.body.clientHeight == document.body.scrollHeight)
		{
			document.body.style.overflowY = 'hidden';
		}
		
        this.setSize(200, 100);
        pos = -5;
		
		for (var i = 0; i < Ext.ux.NotificationMgr.notifications.length; i++)
		{
			pos -= Ext.ux.NotificationMgr.notifications[i].getSize().height + 15;
		}
		
        Ext.ux.NotificationMgr.notifications.push(this);
		
        this.el.alignTo(document.body, "br-br", [ -20, pos ]);
		
        this.el.slideIn('b', {
            duration: 1,
            callback: this.afterShow,
            scope: this
        });
    },
    animHide: function(){
        this.el.ghost("b", {
            duration: 1,
            remove: false,
            callback : function () {
                Ext.ux.NotificationMgr.notifications.remove(this);
				
				if (Ext.ux.NotificationMgr.notifications.length == 0)
				{
					document.body.style.overflowY = Ext.ux.NotificationMgr.originalBodyOverflowY;
				}
				
                this.destroy();
            }.createDelegate(this)

        });
    },
    focus: Ext.emptyFn
});