<template>
  <v-app id="app">
    <MapView />
  </v-app>
</template>

<script>
import MapView from "@/views/MapView";

export default {
  name: 'App',
  components: {
    MapView
  }
}
</script>

<style lang="scss">
.app{
  width: 100%;
  height: 100%;
}

</style>