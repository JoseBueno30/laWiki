import React, { useEffect, useRef, useState } from "react";
import "ol/ol.css";
import { Map, View } from "ol";
import TileLayer from "ol/layer/Tile";
import OSM from "ol/source/OSM";
import { fromLonLat } from "ol/proj";
import { Feature } from "ol";
import Point from "ol/geom/Point";
import VectorSource from "ol/source/Vector";
import VectorLayer from "ol/layer/Vector";
import { Style, Icon } from "ol/style";
import './MapComponent.css';

const MapComponent = () => {
  const mapRef = useRef(null);
  const markerRef = useRef(null);
  const [map, setMap] = useState(null);

  useEffect(() => {
    const lonLat = [-4.4780512, 36.7150865];

    const mapInstance = new Map({
      target: mapRef.current,
      layers: [
        new TileLayer({
          source: new OSM(),
        }),
      ],
      view: new View({
        center: fromLonLat(lonLat),
        zoom: 16,
      }),
    });

    const marker = new Feature({
      geometry: new Point(fromLonLat(lonLat)),
    });

    marker.setStyle(
      new Style({
        image: new Icon({
          anchor: [0.5, 1],
          src: "https://cdn-icons-png.flaticon.com/512/684/684908.png",
          scale: 0.1,
        }),
      })
    );

    const markerLayer = new VectorLayer({
      source: new VectorSource({
        features: [marker],
      }),
    });

    mapInstance.addLayer(markerLayer);

    setMap(mapInstance);
    markerRef.current = marker;

    return () => mapInstance.setTarget(null);
  }, []);

  const handleLocationSearch = async (location) => {
    if (!location) return;

    try {
      const response = await fetch(
        `https://nominatim.openstreetmap.org/search?format=json&q=${location}`
      );
      const results = await response.json();

      if (results.length > 0) {
        const { lon, lat } = results[0];
        const coordinates = fromLonLat([parseFloat(lon), parseFloat(lat)]);

        markerRef.current.setGeometry(new Point(coordinates));

        map.getView().animate({
          center: coordinates,
          duration: 1000,
        });
      } else {
        alert("No se encontró la ubicación.");
      }
    } catch (error) {
      console.error("Error al buscar la ubicación:", error);
    }
  };

  return (
    <div className="map-section">
      <input
        type="text"
        placeholder="Introduce una ubicación"
        className="map-input"
        onKeyDown={(e) => {
          if (e.key === "Enter") handleLocationSearch(e.target.value);
        }}
      />
      <div
        ref={mapRef}
        className="map-container"
      ></div>
    </div>
  );
};

export default MapComponent;
