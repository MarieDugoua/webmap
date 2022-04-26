<template>
  <div class="container-fluid box">
    <div class="img">
      <img src="../../public/airQualityYears.png" alt="airQualityYears">
      <img src="../../public/temperatureEvolutionYears.png" alt="temperatureEvolutionYears">
    </div>
    <div class="dateMap">
      <div class="datePicker">
        <v-row>
          <v-col cols="12" sm="6" md="4">
            <v-menu ref="menu" v-model="menu"
                    :close-on-content-click="false"
                    :return-value.sync="date"
                    transition="scale-transition"
                    offset-y min-width="auto" z-index="1000"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-text-field v-model="date" label="Date" readonly v-bind="attrs" v-on="on"
                ></v-text-field>
              </template>
              <v-date-picker v-model="date" no-title scrollable format="dd/MM/yyyy">
                <v-spacer></v-spacer>
                <v-btn text color="primary" @click="menu = false">Cancel</v-btn>
                <v-btn text color="primary" @click="$refs.menu.save(date)">OK</v-btn>
              </v-date-picker>
            </v-menu>
          </v-col>
          <v-spacer></v-spacer>
        </v-row>

      </div>
      <v-spacer></v-spacer>
      <div class="mapContainer">
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
            <l-tooltip v-if="marker.datas[date] && !marker.datas_temp[date]" :content="marker.name + ', ' + marker.datas[date] + ' pm10'"  />
            <l-tooltip v-if="marker.datas_temp[date] && !marker.datas[date]" :content="marker.name + ', ' + JSON.stringify(marker.datas_temp[date]) + ' C°'"  />
            <l-tooltip v-if="marker.datas_temp[date] && marker.datas[date]" :content="marker.name + ', qualité de l\'aire:  ' + marker.datas[date] + ' pm10' + ', temperature: ' + JSON.stringify(marker.datas_temp[date]) + ' C°'"  />
            <l-tooltip v-else :content="marker.name "  />
          </l-marker>
          <l-tile-layer
              :url="url"
          >
          </l-tile-layer>
        </l-map>
      </div>
    </div>
  </div>
</template>

<script>

import { LMap, LTileLayer, LMarker, LTooltip, LPopup } from "vue2-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

L.Icon.Default.imagePath = "https://unpkg.com/leaflet@1.3.4/dist/images/";
import jsonData from "../../public/database.json"

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
      markers: [],
      markerObjects: null,
      date: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
      menu: false,
    }
  },
  methods: {
    async getJson(){
      try {

        this.markers = await jsonData

      }catch (e) {
        console.log(e)
      }finally {

      }
    },
    displayTooltip(selectedIndex) {
      for (let markerObject of this.markerObjects) {
        markerObject.closeTooltip();
      }
      this.markerObjects[selectedIndex].toggleTooltip();
    },
    zoomUpdated (zoom) {
      this.zoom = zoom;
    },
    centerUpdated (center) {
      this.center = center;
    },
    boundsUpdated (bounds) {
      this.bounds = bounds;

    }
  },
  async mounted() {
    await this.getJson()

    L.Icon.Default.imagePath = "https://unpkg.com/leaflet@1.3.4/dist/images/";
    this.$nextTick(() => {
      this.markerObjects = this.$refs.markersRef.map(ref => ref.mapObject);
    });
  },
}
</script>

<style>
.box{
  width: 100%;
  height: 800px !important;
  display: flex;
  flex-direction: row;
}
.img{
  width: 40%;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
}

.img img{
  width: 80%;
  margin: 0 auto;
}
.dateMap{
  width: 60%;
}
.map {
  width: 950px !important;
  height: 700px !important;
}
</style>