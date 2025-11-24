import axios from "axios";
import router from "../router";
import { useAuthStore } from "../store/auth";

const errorHandler = async (state, msg, config) => {
  switch (state) {
    case 400:
      console.log("login fail" + msg);
      break;
    case 401:
      console.log("axios errorHandler : 401 Auth Fail");
      // Solo intentar refresh si NO estamos ya en el endpoint de refresh o login
      if (config && !config.url?.includes('/auth/refresh') && !config.url?.includes('/auth/login')) {
        const authStore = useAuthStore();
        try {
          // Intentar refrescar el token automáticamente
          const refreshResponse = await authStore.refreshForLogin();
          // Si el refresh es exitoso, NO redirigir - el interceptor manejará la retry
          return;
        } catch (refreshError) {
          // Si falla el refresh, entonces sí redirigir a login
          console.log("Refresh failed, redirecting to login");
          authStore.logout(); // Esto limpiará el token y redirigirá
        }
      }
      break;
    case 403:
      console.log("unauthorized");
      break;
    case 404:
      console.log("not found");
      break;
    default:
      console.log("undefined error" + msg);
  }
};

console.log(import.meta.env.VITE_APP_API_URL);

var instance = axios.create({
  baseURL:
    (import.meta.env.VITE_APP_API_URL ) ,
});


instance.interceptors.request.use(
  (config) => {
    const store = useAuthStore();
    store.get_access_token && (config.headers.Authorization = `Bearer ${store.get_access_token }`);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

instance.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const { response, config } = error;
    if (response) {
      // Solo manejar 401 si no es login o refresh
      if (response.status === 401 && config && !config.url?.includes('/auth/login') && !config.url?.includes('/auth/refresh')) {
        const authStore = useAuthStore();
        // Solo intentar refresh una vez para evitar loops infinitos
        if (!config._retry) {
          config._retry = true;
          try {
            // Intentar refrescar el token en modo silencioso (sin redirigir)
            await authStore.refreshForLogin(true);
            // Si el refresh es exitoso, retry la petición original
            if (authStore.isAuthenticated) {
              config.headers.Authorization = `Bearer ${authStore.get_access_token}`;
              return instance(config);
            }
          } catch (refreshError) {
            // Si falla el refresh, redirigir a login
            console.log('Refresh token failed, logging out');
            authStore.logout();
            return Promise.reject(error);
          }
        }
      }
      // Para otros errores, usar el handler normal
      errorHandler(response.status, response.data, config);
      return Promise.reject(error);
    } else {
      if (!window.navigator.onLine) {
        console.log("offline");
      } else {
        return Promise.reject(error);
      }
    }
  }
);

export default function (method, url, data = null , headers = null) {
  method = method.toUpperCase();

  if( headers ){
    instance.defaults.headers.common = headers;
  }

  switch (method) {
    case "GET":
      let composeUrl = `${url}${data && Object.values(data)[0] ? "/" + Object.values(data)[0] : ""}`;
      let params = {};
      if (data && Object.keys(data).length > 1) {
        let i = 0;
        for (let j in data) if (i++ > 0) params[j] = data[j];
      } else {
        params = null;
      }
      return instance.get(composeUrl, { ...params } );
    case "POST":
      return instance.post(url, data);
    case "PUT":
      return instance.put(url, data);
    case "DELETE":
      return instance.delete(url, data);
    case "PATCH":
      return instance.patch(url, data);
    default:
      console.log("unknow methods" + method);
      return false;
  }
}
