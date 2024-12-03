
import './map-view.css';
import React, { useEffect, useRef } from 'react';
import 'ol/ol.css';
import { Map, View } from 'ol';
import TileLayer from 'ol/layer/Tile';
import OSM from 'ol/source/OSM';
import { fromLonLat } from 'ol/proj';
import VectorLayer from 'ol/layer/Vector';
import VectorSource from 'ol/source/Vector';
import Feature from 'ol/Feature';
import Point from 'ol/geom/Point';
import { Icon, Style } from 'ol/style';

const MapView = ({ lat, lon, zoom, markers=[] }) => {
  const mapRef = useRef();

  useEffect(() => {
    const markerSource = new VectorSource({
      features: markers.map((marker) => {
        return new Feature({
          geometry: new Point(fromLonLat([marker.lon, marker.lat])),
        });
      }),
    });

    const markerLayer = new VectorLayer({
      source: markerSource,
      style: new Style({
        image: new Icon({
          anchor: [0.5, 1],
          src: 'https://cdn-icons-png.flaticon.com/512/64/64113.png', 
          scale: 0.05,
        }),
      }),
    });

    const map = new Map({
      target: mapRef.current,
      layers: [
        new TileLayer({
          source: new OSM(), 
        }),
        markerLayer,
      ],
      view: new View({
        center: fromLonLat([lon, lat]),
        zoom: zoom,
      }),
    });

    return () => map.setTarget(null);
  }, [lon, lat, zoom, markers]);

  return <div ref={mapRef} style={{ width: '50dvh', height: '50dvh' }}></div>;
};

export default MapView;
