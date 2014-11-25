// Animals highlightText function  http://www.extjs.com/forum/showthread.php?t=68599
function highlightText(node, regex, cls, deep) {
    if (typeof(regex) == 'string') {
        regex = new RegExp(regex, "g");
    } else if (!regex.global) {
        throw "RegExp to highlight must use the global qualifier";
    }

    var value, df, m, l, start = 0, highlightSpan;
//  Note: You must add the trim function to the String's prototype
    if ((node.nodeType == 3) && (value = node.data.trim())) {

//      Loop through creating a document DocumentFragment containing text nodes interspersed with
//      <span class={cls}> elements wrapping the matched text.
        while (m = regex.exec(value)) {
            if (!df) {
                df = document.createDocumentFragment();
            }
            if (l = m.index - start) {
                df.appendChild(document.createTextNode(value.substr(start, l)));
            }
            highlightSpan = document.createElement('span');
            highlightSpan.className = cls;
            highlightSpan.appendChild(document.createTextNode(m[0]));
            df.appendChild(highlightSpan);
            start = m.index + m[0].length;
        }

//      If there is a resulting DocumentFragment, replace the original text node with the fragment
        if (df) {
            if (l = value.length - start) {
                df.appendChild(document.createTextNode(value.substr(start, l)));
            }
            node.parentNode.replaceChild(df, node);
        }
    }else{
        if(deep){
            Ext.each(node.childNodes, function(child){
                highlightText(child, regex, cls, deep);
            });
        }
    }
}
// Animals removeHighlighting function
function removeHighlighting(highlightClass, node) {
    var h = Ext.DomQuery.select("span." + highlightClass, node);
    for (var i = 0; i < h.length; i++) {
        var s = h[i], sp = s.parentNode;
        sp.replaceChild(document.createTextNode(s.firstChild.data), s);
        sp.normalize();
    }
}


/*
 * This is the function that actually highlights a text string by
 * adding HTML tags before and after all occurrences of the search
 * term. You can pass your own tags if you'd like, or if the
 * highlightStartTag or highlightEndTag parameters are omitted or
 * are empty strings then the default <font> tags will be used.
 */
function doHighlight(bodyText, searchTerm, highlightStartTag, highlightEndTag)
{
  // the highlightStartTag and highlightEndTag parameters are optional
  if ((!highlightStartTag) || (!highlightEndTag)) {
    highlightStartTag = "<b style='color:blue; background-color:yellow;'>";
    highlightEndTag = "</b>";
  }

  // find all occurences of the search term in the given text,
  // and add some "highlight" tags to them (we're not using a
  // regular expression search, because we want to filter out
  // matches that occur within HTML tags and script blocks, so
  // we have to do a little extra validation)
  var newText = "";
  var i = -1;
  var lcSearchTerm = searchTerm.toLowerCase();
  var lcBodyText = bodyText.toLowerCase();

  while (bodyText.length > 0) {
    i = lcBodyText.indexOf(lcSearchTerm, i+1);
    if (i < 0) {
      newText += bodyText;
      bodyText = "";
    } else {
      // skip anything inside an HTML tag
      if (bodyText.lastIndexOf(">", i) >= bodyText.lastIndexOf("<", i)) {
        // skip anything inside a <script> block
        if (lcBodyText.lastIndexOf("/script>", i) >= lcBodyText.lastIndexOf("<script", i)) {
          newText += bodyText.substring(0, i) + highlightStartTag + bodyText.substr(i, searchTerm.length) + highlightEndTag;
          bodyText = bodyText.substr(i + searchTerm.length);
          lcBodyText = bodyText.toLowerCase();
          i = -1;
        }
      }
    }
  }

  return newText;
}


/*
 * This is sort of a wrapper function to the doHighlight function.
 * It takes the searchText that you pass, optionally splits it into
 * separate words, and transforms the text on the current web page.
 * Only the "searchText" parameter is required; all other parameters
 * are optional and can be omitted.
 */
function highlightSearchTerms(targetcontent, searchText, treatAsPhrase, warnOnFailure, highlightStartTag, highlightEndTag)
{
  // if the treatAsPhrase parameter is true, then we should search for
  // the entire phrase that was entered; otherwise, we will split the
  // search string so that each word is searched for and highlighted
  // individually
  if (treatAsPhrase) {
    searchArray = [searchText];
  } else {
    searchArray = searchText.split(" ");
  }

  if (!targetcontent || typeof(targetcontent) == "undefined") {
    if (warnOnFailure) {
      alert("Sorry, for some reason the text of this page is unavailable. Searching will not work.");
    }
    return false;
  }

  for (var i = 0; i < searchArray.length; i++) {
    targetcontent = doHighlight(targetcontent, searchArray[i], highlightStartTag, highlightEndTag);
  }

  return targetcontent;
}



Ext.namespace('eStation');
// Ext.ns('EMMA');

eStation.myGlobals = {};

Ext.state.Manager.setProvider(new Ext.state.CookieProvider());

Ext.onReady(function(){

    if (!window.console || !console.firebug) {
        var names = ["log", "debug", "info","warn", "error", "assert", "dir", "dirxml", "group", "groupEnd", "time", "timeEnd", "count", "trace", "profile", "profileEnd"];
        window.console = {};
        for (var i = 0; i < names.length; ++i)
            window.console[names[i]] = function() {}
    }

    if (!console){console = {};}
    if (!console.info){console.info = function(){};}

    Ext.QuickTips.init();
 
    // turn on validation errors beside the field globally
    Ext.form.Field.prototype.msgTarget = 'side';

    // console.info(window);

    Ext.BLANK_IMAGE_URL = './js/ext/resources/images/default/s.gif';
 
    Ext.getUrlParam = function(param) {
       var params = Ext.urlDecode(location.search.substring(1));
       return param ? params[param] : params;
    };
//    var Code = Ext.getUrlParam('code');

   eStation.LogFileList = Ext.extend(Ext.grid.GridPanel, {
        // defaults - can be changed from outside
         title:'Log file list'
        ,border:true
        ,frame:true
        ,url:'ajaxphp/systemmonitoring.php'
        ,legendid:-1
    
        ,initComponent:function() {

            // create row actions
//            this.rowActions = new Ext.ux.grid.RowActions({
//                 actions:[{
//    //                 iconIndex:'action1'
//    //                ,qtipIndex:'qtip1'
//                    iconCls:'eye-icon',
//                    qtip:'View logfile.'
//                }]
//                ,width:30
//    //            ,fixed:true
//                ,autoWidth:false
//    //            ,widthIntercept:Ext.isSafari ? 4 : 2
//                ,id:'actions'
//                ,header:'View'
//            });
//            this.rowActions.on('action', this.onRowAction, this);

//            this.mycellActions = new Ext.ux.grid.CellActions({
//                 listeners:{
//                     action:function(grid, record, action, value) {
//                        Ext.ux.Toast.msg('Event: action', 'You have clicked: <b>{0}</b>, action: <b>{1}</b>', value, action);
//                     }
//                     ,beforeaction:function() {
//                        Ext.ux.Toast.msg('Event: beforeaction', 'You can cancel the action by returning false from this event handler.');
//                     }
//                 }
//                 ,callbacks:{
//                     'eye-icon':function(grid, record, action, value) {
//                        Ext.ux.Toast.msg('Callback: icon-undo', 'You have clicked: <b>{0}</b>, action: <b>{1}</b>', value, action);
//                     }
//                 }
//                 ,align:'left'
//            });

            this.store = new Ext.data.Store({
                    id: 'logfileStore',
                    proxy: new Ext.data.HttpProxy({
                        url: 'ajaxphp/systemmonitoring.php',
                        method: 'POST'
                    }),
                    baseParams:{task: "getLogFileList"},
                    reader: new Ext.data.JsonReader({
    //	                root: 'results',
    //	                totalProperty: 'total',
                        id: 'filename'
                    }, [
                        {name: 'filename', mapping: 'filename'},
                        {name: 'filenameformatted', mapping: 'filenameformatted'},
                        {name: 'filesize', mapping: 'filesize'},
                        {name: 'filedate', mapping: 'filedate'},
                        {name: 'filestatus', mapping: 'filestatus'}
                    ])
                    ,sortInfo: {field:'filename', direction:'ASC'}
//                    ,loadMask:{msg: 'Loading data...', msgCls: 'x-mask-loading'}
                    ,loadMask:'Loading data...'                
                    ,autoLoad:true
            });
            
            
            var config = {
                store:this.store
                ,sm: new Ext.grid.RowSelectionModel({singleSelect:true})
                ,columns:[{
                     header:'File name'
                    ,dataIndex:'filenameformatted'
                    ,sortable:true
                    ,width:150
                    ,fixed:false
//                    ,renderer: function(){console.info(store)}
//                            function(){ return '<span style="color:'+dataindex' ; "></div>';}
                },{
                     header:'File size'
                    ,dataIndex:'filesize'
                    ,sortable:true
                    ,width:40
                    ,fixed:false
                },{
                     header:'File date'
                    ,dataIndex:'filedate'
                    ,sortable:true
                    ,width:70
                    ,fixed:false                
                }
//                ,{id:'view',header: "View", width: 30, sortable: false , cellActions:{  iconCls:'eye-icon'
//                                                                                        ,qtip:'View logfile.'
//                                                                                     ,hide:true
//                                                                                     ,hideMode:'display'
//                                                                                 }
//                 }
//                ,this.rowActions
                ]
//                ,plugins:[this.rowActions]
//                ,plugins:[this.mycellActions]
                ,tbar: [{
                    text: 'Log files',
                    iconCls: 'script-icon',
                    scope:this,
                    handler: function() {
                            this.store.load({
                                params: {task: "getLogFileList", filetype:"log", history: this.checked}
                            });
                            Ext.getCmp('ckbHistory').show();
                            this.setTitle('Log file list');
                        }
                },'-',{
                    text: 'Ingest files ',
                    iconCls: 'report_magnify-icon',
                    scope:this,
                    handler: function() {
                            this.store.load({
                                params: {task: "getLogFileList", filetype:"ingest", history: this.checked}
                            });
                            Ext.getCmp('ckbHistory').hide();
                            this.setTitle('Ingest file list');
                        }
                },'-',{
                    text: 'Derived files ',
                    iconCls: 'report_magnify-icon',
                    scope:this,
                    handler: function() {
                            this.store.load({
                                params: {task: "getLogFileList", filetype:"derived", history: this.checked}
                            });
                            Ext.getCmp('ckbHistory').hide();
                            this.setTitle('Derived file list');
                        }
                },'-',{
                    text: 'Report files ',
                    iconCls: 'report_magnify-icon',
                    scope:this,
                    handler: function() {
                            this.store.load({
                                params: {task: "getLogFileList", filetype:"report", history: this.checked}
                            });
                            Ext.getCmp('ckbHistory').hide();
                            this.setTitle('Report file list');
                        }
                },'->',{    
                        xtype: 'checkbox',
                        id:'ckbHistory',
                        boxLabel: 'Show history',
                        labelStyle: 'font-weight:bold;',
                        checked: false,
                        hidden:false,
                        qtip:'Show history files',
                        scope:this,
                        handler:function(ckb) {
                            this.store.load({
                                params: {task: "getLogFileList", history: ckb.checked}
                            });
                        }
                }]
                ,tools:[{
                         id:'refresh'
                        ,qtip:'Refresh log file list'
                        ,handler: function() {
    //						console.info(this);                       
                            this.store.reload();
                         }
                        ,scope:this  
                }]			
                ,viewConfig:{forceFit:true}
//                ,listeners:{
//                    rowclick: function(grid, record, action){
////                        data=grid.getSelectionModel().getSelected().data;
//                        console.info(grid);
//                        console.info(record);
//                        console.info(action);
//                    }
//                    , scope:this
//                }

            }; // eo config object
            // apply config
            Ext.apply(this, Ext.apply(this.initialConfig, config));
    
            // call parent
           eStation.LogFileList.superclass.initComponent.apply(this, arguments);
        } // eo function initComponent

        // {{{  onClick
        ,onClick:function(e, target) {
//                console.info(this.selModel.getSelected());
                var record = this.selModel.getSelected();
                this.getFile(record);

        } // eo onClick
        // }}}

        // {{{
        ,getFile:function(record) {
                   Ext.Ajax.request({
                       method: 'POST',
                       success: function ( result, request ) {

                       },
                       failure: function ( result, request) {

                       },
                       url:'ajaxphp/systemmonitoring.php',
                       params:{ task: "getLogFile",
                                 logfilename:record.data.filename,
                                 dirpath:'' //  will be send without slashes!!!!!!
                       },
                       loadMask:'Loading data...',
                       callback:function(callinfo,responseOK,response ){

                            var response_Text = response.responseText.trim();
                            Ext.getCmp('logfilecontent').setValue(response_Text);
                            eStation.myGlobals.OriginalContent = Ext.getCmp('logfilecontent').getRawValue();
                            eStation.LogfileShowPanel.setTitle('File: ' + record.data.filename);
                       }
                   });
//                   eStation.LogfileShowPanel.setTitle('File: ' + record.data.filename);
//                   eStation.LogfileShowPanel.load({
//                        url:'ajaxphp/systemmonitoring.php',
//                        params:{ task: "getLogFile",
//                                 logfilename:record.data.filename,
//                                 dirpath:'' // 'C:\Documents and Settings\tklooju\Desktop\EMMA log files' will be send without slashes!!!!!!
//                        }
//                    });
        } // eo getFile
        //   }}}

        // {{{
//        ,onRowAction:function(grid, record, action, row, col) {
//
//           switch(action) {
//                case 'eye-icon':
////                    Ext.util.Observable.capture(Ext.getCmp('logfileslist'), function(e){console.log(e);});
//                    this.getFile(record);
//                    break;
//                default:
//                    this.getFile(record);
//                    break;
//            }
//        } // eo onRowAction
//   }}}
       
        /**
         * Load button click handler
         */
//        ,onLoadClick:function() {
//    //		console.info(this.store);
//    //		Ext.ux.Toast.msg('Event: refresh', 'You have clicked the refresh button.', '', '');
//            this.store.load({
//                 url:this.url
//                ,waitMsg:'Loading...'
//                ,params:{task: "getLogFileList"}
//            });
//            // any additional load click processing here
//        } // eo function onLoadClick
    
    }); // eo extend
    // register xtype
    Ext.reg('logfilelist',eStation.LogFileList);
    
    
    
   eStation.LogfileShowPanel = new Ext.Panel({
            id: 'LogfileShowPanel',
            title: 'Log file content',
            border:true,
            frame:true,
            autoScroll:true,
            width:850,
            height:530,
    //        scope:this,
            items:[{
                xtype:'htmleditor',
                id:'logfilecontent',
                autoScroll:true,
                width:830,
                height:468,
                enableAlignments : false,
                enableColors:false,
                enableFont:true,
                enableFontSize:true,
                enableFormat:false,
                enableLinks:false,
                enableLists:false,
                enableSourceEdit:false

//                ,disabled:true
//                autoWidth:true,
//                autoHeight:true
            }
//                {
//                xtype:'box'
//                ,id:'logfilecontent'
//                ,anchor:'',
//                autoScroll:true,
//                width:688,
//                height:588
//                ,autoEl:{
//                      html:'<div id="logfilecontentdiv"></div>'
//                }
//             }
            ],
            tbar: ['  ',
                {
                    xtype: 'textfield',
                    id:'highlightfindstring',
                    fieldLabel: 'Search',
                    labelStyle: 'font-weight:bold;',
                    hidden:false,
                    qtip:'Search in current file.',
                    width:250
    //                scope:this
    //                listeners: {
    //                    keyup: function(txtfield, e) {
    //                             console.info(this);
    //                             console.info(txtfield);
    //                             console.info(e);
    ////                             if(Ext.EventObject.ESC == e.getKey()) {
    ////                                field.onTriggerClick();
    ////                             }
    ////                             else {
    ////                                 var val = this.getRawValue();
    ////                                 var re = new RegExp('.*' + val + '.*', 'i');
    ////                             }
    //                       }
    //                }
                },{
                        text: '',
                        iconCls: 'magnifier-left-icon',
        //                scope:this,
                        handler: function() {
                                    var searchText = Ext.getCmp('highlightfindstring').getValue().trim();

                                    if ( searchText != '') {
    //
                                        var targetcontent = eStation.myGlobals.OriginalContent;    // eStation.myGlobals.OriginalContent is set in logfilelist onRowAction
                                        var textColor = "black";
                                        var bgColor = "yellow";
                                        var treatAsPhrase = false;
                                        var warnOnFailure=false;
                                        var highlightStartTag = "<span style='color:" + textColor + "; background-color:" + bgColor + ";'>";
                                        var highlightEndTag = "</span>";

                                        var highlightedcontent = highlightSearchTerms(targetcontent, searchText, treatAsPhrase, warnOnFailure, highlightStartTag, highlightEndTag);

                                        var contentField = Ext.getCmp('logfilecontent');
                                        Ext.getCmp('logfilecontent').setValue(highlightedcontent);

                                    }
                                    else Ext.getCmp('logfilecontent').setValue(eStation.myGlobals.OriginalContent);   // No search terms so reset content to original content
                            }
                }
            ]
    });



   eStation.logMonitor =  new Ext.Panel({
        id:'sysmonitortab',
        title: 'eStation Log Files',
        renderTo:'logsview',
        border:true,
        frame:true,
        width:1400,
        height:610,       
        iconCls: '',
        autoScroll:true,
//        bodyStyle:'margin:10px 10px 10px 10px; border:1;',  // position:relative; background-color:#f1f1f1;',
        closable:true,
        layout:'table',
        layoutConfig: { columns :   3 },
        defaults:{
             anchor:'100%'
            ,columnWidth: .5
        },
        items:[{
        	html:'<h3>Viewing eStation Log Files</h3>',
        	height:30,
        	border:false,
            frame:false,
        	colspan: 3
        },{
        	xtype:'logfilelist',
            id:'logfileslist',
            border:true,
            frame:true,            
        	width:500,
        	height:530
        },{
        	html:'',
        	width:20,
        	border:false,
            frame:false
        },
        eStation.LogfileShowPanel
       ]
    }).show();

});



// eof
