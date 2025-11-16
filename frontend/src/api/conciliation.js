import axios from 'axios';
import { useAuthStore } from '../store/auth';

// Crear instancia de axios con configuración base
// Usamos la misma baseURL global (VITE_APP_API_URL) y rutas SIN prefijo /api,
// porque el baseURL ya suele incluir /api (ej: http://localhost:5001/api)
const instance = axios.create({
    baseURL: import.meta.env.VITE_APP_API_URL
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