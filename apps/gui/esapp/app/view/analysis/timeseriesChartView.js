
Ext.define("esapp.view.analysis.timeseriesChartView",{
    "extend": "Ext.window.Window",
    "controller": "analysis-timeserieschartview",
    "viewModel": {
        "type": "analysis-timeserieschartview"
    },

    xtype: 'timeserieschart-window',

    requires: [
        'esapp.view.analysis.timeseriesChartViewModel',
        'esapp.view.analysis.timeseriesChartViewController',

        'Ext.window.Window',
        'Ext.toolbar.Toolbar'
    ],

    //title: '<span class="panel-title-style">MAP title</span>',
    margin: '0 0 0 0',
    layout: {
        type: 'border'
    },
    width:850,
    height:800,
    minWidth:400,
    minHeight:350,
    // glyph : 'xf080@FontAwesome',
    constrain: true,
    autoShow : false,
    closeable: true,
    closeAction: 'destroy', // 'hide',
    maximizable: true,
    collapsible: true,

    header: {
        titlePosition: 2,
        titleAlign: "center"
    },

    wkt: null,

    tools: [
    {
        type: 'gear',
        tooltip: 'Show/hide time series chart tools menu',
        callback: function (tswin) {
            // toggle hide/show toolbar and adjust map size.
            var sizeWinBody = [];
            var tsToolbar = tswin.getDockedItems('toolbar[dock="top"]')[0];
            var widthToolbar = tsToolbar.getWidth();
            var heightToolbar = tsToolbar.getHeight();
            if (tsToolbar.hidden == false) {
                tsToolbar.setHidden(true);
                sizeWinBody = [document.getElementById(tswin.id + "-body").offsetWidth, document.getElementById(tswin.id + "-body").offsetHeight+heightToolbar];
            }
            else {
                tsToolbar.setHidden(false);
                sizeWinBody = [document.getElementById(tswin.id + "-body").offsetWidth, document.getElementById(tswin.id + "-body").offsetHeight-heightToolbar];
            }
            tswin.map.setSize(sizeWinBody);
        }
    }],

    initComponent: function () {
        var me = this;

        me.frame = false;
        me.border= false;
        me.bodyBorder = false;

        me.wkt = this.wkt;

        me.tbar = Ext.create('Ext.toolbar.Toolbar', {
            dock: 'top',
            autoShow: true,
            alwaysOnTop: true,
            floating: false,
            hidden: false,
            border: false,
            shadow: false,
            padding:0,
            items: [{
                text: 'Chart properties',
                iconCls: 'chart-curve_edit',
                scale: 'medium'
                //,handler: 'openChartProperties'
            },'->',{
                text: 'Download timeseries',
                iconCls: 'fa fa-download fa-2x',
                scale: 'medium'
                //,handler: 'tsDownload'
            },{
                text: 'Save chart',
                iconCls: 'fa fa-floppy-o fa-2x',
                scale: 'medium'
                //,handler: 'saveChart'
            }]
        });


        me.name ='tschartwindow_' + me.id;

        me.items = [{
            region: 'center',
            items: [{
                xtype: 'container',
                layout:'fit',
                reference:'tschartcontainer_'+me.id,
                html: '<div id="tschart_' + me.id + '"></div>'

            }]
        }];

        me.listeners = {
            afterrender: function () {

                var chartwidth = document.getElementById(me.id + "-body").offsetWidth;
                var chartheight = document.getElementById(me.id + "-body").offsetHeight

                new Highcharts.Chart({
                    chart: {
                        renderTo:'tschart_'+me.id,
                        height:800,
                        width:800,
                        zoomType: 'xy'
                    },
                    title: {
                        text: 'Average Monthly Weather Data for Tokyo'
                    },
                    subtitle: {
                        text: 'Source: WorldClimate.com'
                    },
                    xAxis: [{
                        categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                        crosshair: true
                    }],
                    yAxis: [{ // Primary yAxis
                        labels: {
                            format: '{value}°C',
                            style: {
                                color: Highcharts.getOptions().colors[2]
                            }
                        },
                        title: {
                            text: 'Temperature',
                            style: {
                                color: Highcharts.getOptions().colors[2]
                            }
                        },
                        opposite: true

                    }, { // Secondary yAxis
                        gridLineWidth: 0,
                        title: {
                            text: 'Rainfall',
                            style: {
                                color: Highcharts.getOptions().colors[0]
                            }
                        },
                        labels: {
                            format: '{value} mm',
                            style: {
                                color: Highcharts.getOptions().colors[0]
                            }
                        }

                    }, { // Tertiary yAxis
                        gridLineWidth: 0,
                        title: {
                            text: 'Sea-Level Pressure',
                            style: {
                                color: Highcharts.getOptions().colors[1]
                            }
                        },
                        labels: {
                            format: '{value} mb',
                            style: {
                                color: Highcharts.getOptions().colors[1]
                            }
                        },
                        opposite: true
                    }],
                    tooltip: {
                        shared: true
                    },
                    legend: {
                        layout: 'vertical',
                        align: 'left',
                        x: 80,
                        verticalAlign: 'top',
                        y: 55,
                        floating: true,
                        backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'
                    },
                    series: [{
                        name: 'Rainfall',
                        type: 'column',
                        yAxis: 1,
                        data: [49.9, 71.5, 106.4, 129.2, 144.0, 176.0, 135.6, 148.5, 216.4, 194.1, 95.6, 54.4],
                        tooltip: {
                            valueSuffix: ' mm'
                        }

                    }, {
                        name: 'Sea-Level Pressure',
                        type: 'spline',
                        yAxis: 2,
                        data: [1016, 1016, 1015.9, 1015.5, 1012.3, 1009.5, 1009.6, 1010.2, 1013.1, 1016.9, 1018.2, 1016.7],
                        marker: {
                            enabled: false
                        },
                        dashStyle: 'shortdot',
                        tooltip: {
                            valueSuffix: ' mb'
                        }

                    }, {
                        name: 'Temperature',
                        type: 'spline',
                        data: [7.0, 6.9, 9.5, 14.5, 18.2, 21.5, 25.2, 26.5, 23.3, 18.3, 13.9, 9.6],
                        tooltip: {
                            valueSuffix: ' °C'
                        }
                    }]
                });

            }
            // The resize handle is necessary to set the map!
            ,resize: function () {
                //var size = [document.getElementById(this.id + "-body").offsetWidth, document.getElementById(this.id + "-body").offsetHeight];
                //this.map.setSize(size);
                //
                //this.getController().redrawTimeLine(this);
            }
            ,move: function () {
                //this.getController().redrawTimeLine(this);
            }

        };

        me.callParent();
    }
});
