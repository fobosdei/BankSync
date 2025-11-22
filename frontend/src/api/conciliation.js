import axios from 'axios';
import { useAuthStore } from '../store/auth';

// Crear instancia de axios con configuración base
// Usamos el proxy de Vite en desarrollo (/api) o la URL configurada en VITE_APP_API_URL
const instance = axios.create({
    baseURL: import.meta.env.VITE_APP_API_URL || '/api'
});

// Interceptor para agregar el token de autenticación
instance.interceptors.request.use(
    (config) => {
        const store = useAuthStore();
        if (store.get_access_token) {
            config.headers.Authorization = `Bearer ${store.get_access_token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Interceptor para manejar errores 401 (token expirado)
instance.interceptors.response.use(
    (response) => {
        return response;
    },
    async (error) => {
        const { response, config } = error;
        if (response && response.status === 401 && config) {
            const store = useAuthStore();
            // Solo intentar refresh si no es login o refresh
            if (!config.url?.includes('/auth/login') && !config.url?.includes('/auth/refresh')) {
                // Solo intentar refresh una vez para evitar loops
                if (!config._retry) {
                    config._retry = true;
                    try {
                        // Intentar refrescar el token en modo silencioso
                        await store.refreshForLogin(true);
                        // Si el refresh es exitoso, retry la petición original
                        if (store.isAuthenticated) {
                            config.headers.Authorization = `Bearer ${store.get_access_token}`;
                            return instance(config);
                        }
                    } catch (refreshError) {
                        // Si falla el refresh, redirigir a login
                        console.log('Refresh token failed, logging out');
                        store.logout();
                        return Promise.reject(error);
                    }
                }
            }
        }
        return Promise.reject(error);
    }
);

/**
 * Realizar conciliación completa con PDF y Excel
 */
export const apiConciliar = (pdfFile, excelFile) => {
    const formData = new FormData();
    formData.append('extracto_pdf', pdfFile);
    formData.append('movimientos_excel', excelFile);
    
    console.log(' Enviando solicitud a:', `${instance.defaults.baseURL}/conciliation/conciliar`);
    console.log(' Archivos:', {
        pdf: pdfFile?.name,
        excel: excelFile?.name
    });
    
    return instance.post('/conciliation/conciliar', formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        },
        timeout: 300000, // 5 minutos timeout para procesos largos
        onUploadProgress: (progressEvent) => {
            const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
            console.log(` Progreso de upload: ${percentCompleted}%`);
        }
    });
};

/**
 * Probar extracción de PDF solamente
 */
export const apiProbarPDF = (pdfFile) => {
    const formData = new FormData();
    formData.append('archivo_pdf', pdfFile);
    
    console.log(' Probando extracción PDF en:', `${instance.defaults.baseURL}/conciliation/probar-pdf`);
    
    return instance.post('/conciliation/probar-pdf', formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        },
        timeout: 120000 // 2 minutos timeout
    });
};

/**
 * Verificar estado del servicio de conciliación
 */
export const apiHealthCheck = () => {
    console.log('🏥 Health check en:', `${instance.defaults.baseURL}/conciliation/health`);
    return instance.get('/conciliation/health');
};

/**
 * Obtener historial de conciliaciones guardadas en BD
 */
export const apiGetHistorial = () => {
    return instance.get('/conciliation/historial');
};

/**
 * Obtener resumen agregado para el dashboard
 */
export const apiGetDashboardResumen = () => {
    return instance.get('/conciliation/dashboard-resumen');
};

/**
 * Descargar reporte de conciliación (si lo implementas después)
 */
export const apiDescargarReporte = (conciliacionId) => {
    return instance.get(`/conciliation/reporte/${conciliacionId}`, {
        responseType: 'blob'
    });
};

/**
 * Obtener transacciones del usuario
 */
export const apiGetTransactions = (uploadId = null, limit = 100, offset = 0) => {
    const params = new URLSearchParams();
    if (uploadId) params.append('upload_id', uploadId);
    params.append('limit', limit.toString());
    params.append('offset', offset.toString());
    return instance.get(`/conciliation/transactions?${params.toString()}`);
};

/**
 * Obtener lista de bancos del usuario
 */
export const apiGetBanks = () => {
    return instance.get('/conciliation/banks');
};