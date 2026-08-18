// utils/ToastManager.js
class ToastManager {
    static toasts = [];
    static listeners = [];
  
    static addToast(message) {
      const newToast = { message: message.message, type: message.type, id: Date.now() };
      this.toasts = [newToast, ...this.toasts].slice(0, 5);
      this.notify();
      setTimeout(() => this.removeToast(newToast.id), 5000);
    }

    static error(message) {
        this.addToast({ message, type: 'error' });
    }

    static success(message) {
        this.addToast({ message, type: 'success' });
    }

    static warning(message) {
        this.addToast({ message, type: 'warning' });
    }
  
    static removeToast(id) {
      this.toasts = this.toasts.filter((toast) => toast.id !== id);
      this.notify();
    }
  
    static subscribe(listener) {
      this.listeners.push(listener);
      listener(this.toasts);
    }
  
    static unsubscribe(listener) {
      this.listeners = this.listeners.filter((l) => l !== listener);
    }
  
    static notify() {
      this.listeners.forEach((listener) => listener(this.toasts));
    }
  }
  
  export default ToastManager;
  