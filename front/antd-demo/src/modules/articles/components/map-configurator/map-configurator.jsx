import './map-configurator.css';
import React, { useEffect, useRef, useState } from 'react';
import { Button, Flex, Row, Col } from 'antd';
import 'ol/ol.css';
import { Map, View } from 'ol';
import TileLayer from 'ol/layer/Tile';
import OSM from 'ol/source/OSM';
import { fromLonLat, toLonLat } from 'ol/proj';
import { Overlay } from 'ol';
import { Feature } from 'ol';
import { Point } from 'ol/geom';
import VectorSource from 'ol/source/Vector';
import VectorLayer from 'ol/layer/Vector';
import { Icon, Style } from 'ol/style';
import { useTranslation } from "react-i18next";

const MapConfigurator = ({ onSave }) => {
  const mapRef = useRef(null);
  const [markers, setMarkers] = useState([]);
  const [vectorLayer, setVectorLayer] = useState(null);
  const [centerMarkerFeature, setCenterMarkerFeature] = useState(null);
  const [userLocation, setUserLocation] = useState([0, 0]);

  const { t } = useTranslation();

  useEffect(() => {
    if (!mapRef.current) {
      const map = new Map({
        target: 'map-container',
        layers: [
          new TileLayer({
            source: new OSM(),
          }),
        ],
        view: new View({
          center: fromLonLat(userLocation), 
          zoom: 13,
        }),
      });

      const vectorSource = new VectorSource();
      const vectorLayer = new VectorLayer({
        source: vectorSource,
      });
      map.addLayer(vectorLayer);
      setVectorLayer(vectorSource);

      mapRef.current = map;

      const centerFeature = new Feature({
        geometry: new Point(map.getView().getCenter()),
      });

      centerFeature.setStyle(
        new Style({
          image: new Icon({
            anchor: [0.5, 1],
            src: 'https://cdn-icons-png.flaticon.com/512/64/64113.png',
            scale: 0.1,
          }),
        })
      );
      vectorSource.addFeature(centerFeature);
      setCenterMarkerFeature(centerFeature);

      map.on('click', (evt) => {
        const coordinate = evt.coordinate;
        addMarker(coordinate);
      });

      map.on('moveend', () => {
        const newCenter = map.getView().getCenter();
        centerFeature.setGeometry(new Point(newCenter));
      });

      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition((position) => {
          const { latitude, longitude } = position.coords;
          setUserLocation([longitude, latitude]);
          map.getView().setCenter(fromLonLat([longitude, latitude]));
        }, () => {
          message.warning("No se pudo obtener la ubicación.");
        });
      }
    }
  }, [userLocation]);

  const addMarker = (coordinate) => {
    const iconFeature = new Feature({
      geometry: new Point(coordinate),
    });

    iconFeature.setStyle(
      new Style({
        image: new Icon({
          anchor: [0.5, 1],
          src: 'https://cdn-icons-png.flaticon.com/512/64/64113.png',
          scale: 0.05,
        }),
      })
    );

    vectorLayer.addFeature(iconFeature);
    setMarkers([...markers, coordinate]);
  };

  const generateWikitextTag = () => {
    const markerTags = markers.map((marker) => {
      console.log(toLonLat(marker))
      const [lon, lat] = toLonLat(marker);
      return `{"lat":${lat},"lon":${lon}},`;
    });
    const view = mapRef.current.getView();
    const center = toLonLat(view.getCenter());
    const zoom = view.getZoom();
    return `<MapView lat="${center[1]}" lon="${center[0]}" zoom="${zoom}" markers={[${markerTags.join('')}]}/>`;
  };

  const handleSave = () => {
    const wikitextTag = generateWikitextTag();
    onSave(wikitextTag);
  };

  return (
    <div>
        <Row
          style={{paddingBottom:5, width:"100%"}}
          tabIndex={0}
          justify="space-around"
          align="middle"
        >
          <Col
        sm={12}
        xs={24}
        align="center"
      >
        <Button onClick={() => addMarker(mapRef.current.getView().getCenter())} type="primary">
          {t("edit.add-marker")}
        </Button>
      </Col>
      <Col
        sm={12}
        xs={24}
        align="center"
      >
        <Button onClick={handleSave} style={{ marginLeft: '10px' }}>
        {t("edit.save-map")}
        </Button>
      </Col>

        </Row>
      <div id="map-container" style={{ width: '100%', height: '70vh' }}></div>
    </div>
  );
};

export default MapConfigurator;
