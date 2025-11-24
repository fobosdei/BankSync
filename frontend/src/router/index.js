// src/router/index.js
import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import DashboardView from '../views/DashboardView.vue'
import ProfileView from '../views/ProfileView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import LogoutView from '../views/LogoutView.vue'
import RefreshView from '../views/RefreshView.vue'
import { useAuthStore } from '../store/auth'

const routes = [
    {
        path: '/',
        name: 'Login',
        component: LoginView,
    },
    {
        path: '/home',
        name: 'Home',
        component: DashboardView,
        meta: { requiresAuth: true },
    },
    {
        path: '/dashboard',
        name: 'Dashboard',
        component: DashboardView,
        meta: { requiresAuth: true },
    },
    {
        path: '/register',
        name: 'Register',
        component: RegisterView,
    },
    {
        path: '/profile',
        name: 'Profile',
        component: ProfileView,
        meta: { requiresAuth: true },
    },
    {
        path: '/logout',
        name: 'Logout',
        component: LogoutView,
    },
    {
        path: '/refresh',
        name: 'Refresh',
        component: RefreshView,
    },
]

const router = createRouter({
    history: createWebHashHistory(),
    routes,
})

router.beforeEach(async (to, from, next) => {
    const auth = useAuthStore();
    
    // Si la ruta requiere autenticación
    if (to.matched.some((record) => record.meta.requiresAuth)) {
        // Verificar autenticación - el store ya carga el token desde localStorage al inicializar
        if (auth.isAuthenticated) {
            next();
            return;
        }
        
        // Si no está autenticado pero tiene token guardado, verificar validez
        if (auth.get_access_token && auth.get_expires_in) {
            const now = Date.now();
            const expiresIn = auth.get_expires_in;
            
            // Si el token no ha expirado (con margen de 1 minuto), permitir acceso
            // El computed puede fallar si hay un problema de timing, pero el token es válido
            if (expiresIn > (now + 60000)) {
                next();
                return;
            }
            
            // Si el token está por expirar o expiró, intentar refrescar silenciosamente
            if (expiresIn > now) {
                // Aún válido pero cerca de expirar, intentar refresh en background
                try {
                    await auth.refreshForLogin(true);
                    if (auth.isAuthenticated) {
                        next();
                        return;
                    }
                } catch (e) {
                    console.log('Background refresh failed, but token still valid');
                    // Continuar si el refresh falla pero el token aún es válido
                    next();
                    return;
                }
            } else {
                // Token expirado, intentar refrescar
                try {
                    await auth.refreshForLogin(true);
                    if (auth.isAuthenticated) {
                        next();
                        return;
                    }
                } catch (e) {
                    console.log('Token expired and refresh failed, redirecting to login');
                    // Si falla el refresh, redirigir a login
                    next("/");
                    return;
                }
            }
        }
        
        // Si no tiene token guardado, redirigir a login
        next("/");
    } else {
        // Ruta pública (login, register), permitir acceso
        next();
    }
})

export default router;