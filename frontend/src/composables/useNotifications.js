import { useDialogStore } from '../store/dialog';

/**
 * Composable para mostrar notificaciones al usuario
 * Proporciona métodos para success, error, warning e info
 */
export function useNotifications() {
    const dialogStore = useDialogStore();

    const showSuccess = (message, title = 'Éxito') => {
        dialogStore.setSuccess({
            title,
            firstLine: message,
            secondLine: ''
        });
        setTimeout(() => dialogStore.reset(), 3000);
    };

    const showError = (message, title = 'Error') => {
        dialogStore.setError({
            title,
            firstLine: message,
            secondLine: ''
        });
        setTimeout(() => dialogStore.reset(), 4000);
    };

    const showWarning = (message, title = 'Advertencia') => {
        dialogStore.setWarning({
            title,
            firstLine: message,
            secondLine: ''
        });
        setTimeout(() => dialogStore.reset(), 3500);
    };

    const showInfo = (message, title = 'Información') => {
        dialogStore.setInfo({
            title,
            firstLine: message,
            secondLine: ''
        });
        setTimeout(() => dialogStore.reset(), 3000);
    };

    return {
        showSuccess,
        showError,
        showWarning,
        showInfo
    };
}
