import axios from 'axios';
import { useAuthStore } from '../store/auth';

// Crear instancia de axios con configuración base
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
    
    return instance.post('/conciliation/conciliar', formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
};

/**
 * Probar extracción de PDF solamente
 */
export const apiProbarPDF = (pdfFile) => {
    const formData = new FormData();
    formData.append('archivo_pdf', pdfFile);
    
    return instance.post('/conciliation/probar-pdf', formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
};

/**
 * Verificar estado del servicio de conciliación
 */
export const apiHealthCheck = () => {
    return instance.get('/conciliation/health');
};
