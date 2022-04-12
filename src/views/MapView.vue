<template>
  <l-map
      class="map"
      ref="map"
      :zoom="zoom"
      :center="center"
      @update:zoom="zoomUpdated"
      @update:center="centerUpdated"
      @update:bounds="boundsUpdated"
  >
    <l-marker
        v-for="(marker, index) in markers"
        :key="index"
        :lat-lng="marker.coordinates"
    >
      <l-tooltip :content="marker.name" />
    </l-marker>
    <l-tile-layer
        :url="url"
    >
    </l-tile-layer>
  </l-map>
</template>

<script>

import { LMap, LTileLayer, LMarker, LTooltip, LPopup } from "vue2-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

L.Icon.Default.imagePath = "https://unpkg.com/leaflet@1.3.4/dist/images/";

export default {
  name: 'MapView',
  components: {
    "l-map": LMap,
    "l-tile-layer": LTileLayer,
    "l-marker": LMarker,
    "l-tooltip": LTooltip,
    "l-popup": LPopup
  },
  data () {
    return {
      url: "http://{s}.tile.osm.org/{z}/{x}/{y}.png",
      attribution:
          '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      center: [ 44.837789, -0.57918 ],
      zoom: 5,
      markers: [
        {id: 1, name: 'Bordeaux', coordinates: { lat: 44.837789, lng: 	-0.57918 }},
        {id: 2, name: 'Annecy', coordinates: { lat: 45.8615248, lng: 6.1673232 }},
        {id: 3, name: 'Londre', coordinates: { lat: 51.509093, lng: -0.094151 }},
        {id: 4, name: 'Rome', coordinates: { lat: 41.902784, lng: 12.496366 }},
        {id: 5, name: 'Valence', coordinates: { lat: 44.933393, lng: 4.89236 }},
      ],
      markerObjects: null
    }
  },
  mounted: function() {
    L.Icon.Default.imagePath = "https://unpkg.com/leaflet@1.3.4/dist/images/";
    this.$nextTick(() => {
      this.markerObjects = this.$refs.markersRef.map(ref => ref.mapObject);
    });
  },
  methods: {
    displayTooltip(selectedIndex) {
      for (let markerObject of this.markerObjects) {
        markerObject.closeTooltip();
      }
      this.markerObjects[selectedIndex].toggleTooltip();
    },
    zoomUpdated (zoom) {
      this.zoom = zoom;
      console.log(this.markers)
    },
    centerUpdated (center) {
      this.center = center;
    },
    boundsUpdated (bounds) {
      this.bounds = bounds;
    }
  }
}
</script>

<style>
.map {
  position: absolute;
  width: 100%;
  height: 100%;
  overflow :hidden
}
</style>