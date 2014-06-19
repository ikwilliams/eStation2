/*!
 * Ext JS Library 3.4.0
 * Copyright(c) 2006-2011 Sencha Inc.
 * licensing@sencha.com
 * http://www.sencha.com/license
 */
Ext.ux.BubblePanel = Ext.extend(Ext.Window, {
    baseCls: 'x-bubble',
    frame: true
});


/**
 * Overrides the Ext.TabPanel to add .setTabTitle() function
 */
Ext.override(Ext.TabPanel, {
    /**
     * Set the title of a specific tab
     */
    setTabTitle: function( tabNo, newTitle ) {
        // make sure we have a number and tab exists
        if( tabNo>=0 && !Ext.isEmpty( this.getTabEl(tabNo))) {
            var tabEl = this.getTabEl(tabNo); // walk down dom, update title span
            tabEl.textContent = newTitle;
//            var t = Ext.get(tabEl.id);
//            var tt = t.down('x-tab-strip-text ');
//            tt.innerHTML = newTitle;
        }
     }
 });
