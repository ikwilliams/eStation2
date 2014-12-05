Ext.define('esapp.view.analysis.mapViewController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.analysis-mapview'

    ,toggleLink: function(btn, event) {
        var mapviewwin = btn.up().up();
        console.info(mapviewwin);
        console.info(mapviewwin.up());
        console.info(mapviewwin.mapView);
        console.info(mapviewwin.commonMapView);

        if (btn.pressed) {
            mapviewwin.map.setView(mapviewwin.mapView);
            btn.setText('Link');
        }
        else {
            mapviewwin.map.setView(mapviewwin.up().commonMapView);
            btn.setText('Unlink');
        }
    }
});
