Ext.define('esapp.view.analysis.analysisMainController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.analysis-analysismain'

    ,newMapView: function(btn, event) {
        var analysismain = btn.up().up();

        var newMapViewWin = new esapp.view.analysis.mapView({
            layers: [
                new ol.layer.Image({
                    source: new ol.source.ImageWMS({
                        url: 'getlayer',
                        crossOrigin: 'anonymous',
                        attributions: [new ol.Attribution({
                            html: '&copy; ' +
                                '<a href="https://ec.europa.eu/jrc/' +
                                'eStation 2 </a>'
                        })],
                        params: {
                            // 'LAYERS': 'ch.swisstopo.pixelkarte-farbe-pk1000.noscale',
                            'FORMAT': 'image/jpeg'
                        },
                        serverType: /** @type {ol.source.wms.ServerType} */ ('mapserver')
                    })
                })
//                Request URL:
//                  http://h05-dev-vm19.ies.jrc.it/esapp/getlayer?
//                  SERVICE=WMS&
//                  VERSION=1.3.0&
//                  REQUEST=GetMap&
//                  FORMAT=image%2Fjpeg&
//                  TRANSPARENT=true&
//                  CRS=EPSG%3A3857&
//                  STYLES=&
//                  WIDTH=736&
//                  HEIGHT=782&
//                  BBOX=-4863270.2540311385%2C-7205400.673576976%2C9538688.86734863%2C8096680.892889029

//                new ol.layer.Tile({
//                    source: new ol.source.MapQuest({layer: 'sat'})
//                })
            ]
        });
        analysismain.add(newMapViewWin);
        newMapViewWin.show();
    }

    ,toggleBackgroundlayer: function(btn, event) {
        var analysismain = btn.up().up();
        var i, ii;
        for (i = 0, ii = analysismain.backgroundLayers.length; i < ii; ++i) {
            analysismain.backgroundLayers[i].setVisible(!btn.pressed);
        }
        if (btn.pressed) btn.setText('Show Background layer');
        else btn.setText('Hide Background layer');
    }

});
