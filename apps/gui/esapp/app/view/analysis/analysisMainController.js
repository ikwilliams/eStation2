Ext.define('esapp.view.analysis.analysisMainController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.analysis-analysismain'

    ,newMapView: function(btn, event) {
        var analysismain = btn.up().up();

        var newMapViewWin = new esapp.view.analysis.mapView({
            layers: [
                new ol.layer.Tile({
                    source: new ol.source.MapQuest({layer: 'sat'})
                })
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
