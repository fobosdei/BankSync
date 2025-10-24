<script setup>
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import NavBar from "./components/NavBar.vue";
import Dialog from "./components/Dialog.vue";
import Loading from "./components/Loading.vue";

const route = useRoute();
const showNavBar = computed(() => route.path !== '/' && route.path !== '/register');
</script>

<template>
  <div id="app">
    <NavBar v-if="showNavBar" />
    <router-view />
    <Loading />
    <Dialog />
  </div>
</template>

<script>
export default {
  name: 'App',
  components: {
    NavBar,
  },
}
</script>

<style scoped>

</style>
