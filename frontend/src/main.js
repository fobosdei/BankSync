import { createApp } from "vue";
import axios from 'axios';
import { createPinia } from 'pinia';

import App from './App.vue';
import router from './router';

import './style.css';


axios.defaults.withCredentials = true;
// Usar el proxy de Vite en desarrollo (sin /api porque el proxy ya lo maneja)
// O usar la URL directa si VITE_APP_API_URL está configurada
axios.defaults.baseURL = import.meta.env.VITE_APP_API_URL || '/api';  // Usa el proxy de Vite

const pinia = createPinia()

createApp(App)
  .use(pinia)
  .use(router)
  .mount("#app");