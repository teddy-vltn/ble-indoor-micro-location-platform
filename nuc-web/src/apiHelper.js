import axios from 'axios';
import ToastManager from './components/toasts/ToastManager';

export const apiRequest = async ({ url, method, data = {}, onSuccess, onError, onFinally }) => {
    try {
        const response = await axios({ url, method, data });
        if (onSuccess) onSuccess(response);
        if (response.data.message) {
            ToastManager.addToast({ type: 'success', message: response.data.message  });
        }
    } catch (error) {
        const message = error.response?.data?.message || error.message;
        if (onError) onError(error);
        ToastManager.addToast({ type: 'error', message });
        console.error(error);
    } finally {
        if (onFinally) onFinally();
    }
};
