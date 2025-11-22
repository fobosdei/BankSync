import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { apiLogin, apiRefresh, apiLogout } from '../api/auth'
import { useLoadingStore } from './loading';
import { useDialogStore } from './dialog';
import router from '../router';

export const useAuthStore = defineStore('auth', () => {
    // Intentar cargar token desde localStorage al inicializar
    const savedToken = localStorage.getItem('bankSync_access_token');
    const savedExpiresIn = localStorage.getItem('bankSync_expires_in');
    
    const access_token = ref(savedToken ? savedToken : null);
    const expires_in = ref(savedExpiresIn ? parseInt(savedExpiresIn, 10) : null);

    const loadingStore = useLoadingStore();
    const dialogStore = useDialogStore();

    // Función helper para guardar en localStorage
    const saveToStorage = (token, expires) => {
        if (token) {
            localStorage.setItem('bankSync_access_token', token);
        } else {
            localStorage.removeItem('bankSync_access_token');
        }
        if (expires) {
            localStorage.setItem('bankSync_expires_in', expires.toString());
        } else {
            localStorage.removeItem('bankSync_expires_in');
        }
    };

    const isAuthenticated = computed(() => {
        if (!access_token.value || !expires_in.value) {
            return false;
        }
        // Verificar que el token no haya expirado (con margen de 1 minuto)
        // expires_in está en milisegundos (timestamp de expiración)
        const now = Date.now();
        const expiresAt = expires_in.value;
        // El token es válido si expira en más de 1 minuto
        const isValid = expiresAt > (now + 60000);
        return isValid && access_token.value.length > 0;
    });
    const get_access_token = computed(() => access_token.value);
    const get_expires_in = computed(() => expires_in.value);

    async function login(form) {
        access_token.value = null;
        expires_in.value = null;

        loadingStore.setLoading();

        apiLogin(form)
        .then(res => {
            access_token.value = res.data.access_token;
            expires_in.value = res.data.expires_in;
            
            // Guardar en localStorage para persistencia
            saveToStorage(res.data.access_token, res.data.expires_in);

            dialogStore.setSuccess({
                title: 'Login Success',
                firstLine: 'You can login now',
                secondLine: 'This dialog will close in 1 seconds'
            });
        })
        .catch(err => {
            dialogStore.setError({
                title: 'Login Failed',
                firstLine: 'Please check your input',
                secondLine: 'This dialog will close in 1 seconds'
            });
            access_token.value = null;
            expires_in.value = null;
            saveToStorage(null, null);
        })
        .finally( () => {
            loadingStore.clearLoading();
            setTimeout(() => {
                dialogStore.reset();

                console.log(isAuthenticated.value);
                console.log(access_token.value);
                console.log(expires_in.value);
                console.log(Date.now());    

                if (isAuthenticated.value){
                    router.push('/home');
                    console.log('pushed to home');
                }

            }, 1000);
        })

    }

    function logout() {
        apiLogout()
        .then(res => {
            access_token.value = null;
            expires_in.value = null;
            saveToStorage(null, null); // Limpiar localStorage

            dialogStore.setSuccess({
                title: 'Logout Success',
                firstLine: 'Redirecting to login page 1 second',
                secondLine: ''
            });

            setTimeout(() => {
                dialogStore.reset();
                router.push('/');
            },1000);
        })
        .catch(err => {
            // Aunque falle el logout en el servidor, limpiamos el estado local
            access_token.value = null;
            expires_in.value = null;
            saveToStorage(null, null);
            router.push('/');
        });
    }

    function refresh() {
        loadingStore.setLoading();

        apiRefresh()
        .then(res => {
            access_token.value = res.data.access_token;
            expires_in.value = res.data.expires_in;
            saveToStorage(res.data.access_token, res.data.expires_in); // Guardar en localStorage

            dialogStore.setSuccess({
                title: 'Refresh Success',
                firstLine: 'Redirecting to profile page',
                secondLine: 'This dialog will close in 1 seconds'
            });
        })
        .catch(err => {
            console.log(err);
            access_token.value = null;
            expires_in.value = null;
            saveToStorage(null, null); // Limpiar si falla

            dialogStore.setError({
                title: 'Refresh Failed',
                firstLine: 'Please login again',
                secondLine: 'This dialog will close in 1 seconds'
            });
        })
        .finally( () => {
            setTimeout(() => {
                if (isAuthenticated.value){
                    router.push('/home');
                    console.log('pushed to home');
                }
                else{
                    router.push('/');
                    console.log('pushed to login');
                }
                
                dialogStore.reset();
                loadingStore.clearLoading();

            }, 1000);
        })
    }

    function refreshForLogin() {
        // NO mostrar loading ni redirigir cuando se usa desde interceptor
        return apiRefresh()
        .then(res => {
            access_token.value = res.data.access_token;
            expires_in.value = res.data.expires_in;
            saveToStorage(res.data.access_token, res.data.expires_in); // Guardar en localStorage
            return res; // Retornar la respuesta para que el interceptor pueda usar el token
        })
        .catch(err => {
            console.log(err);
            access_token.value = null;
            expires_in.value = null;
            saveToStorage(null, null); // Limpiar si falla
            throw err; // Re-lanzar el error para que el interceptor lo maneje
        });
    }

    return {
        access_token,
        get_access_token,
        get_expires_in,
        isAuthenticated,
        login,
        logout,
        refresh,
        refreshForLogin
    }
})