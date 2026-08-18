import numpy as np

def kalman_filter_rssi(rssi_values, Q=1, R=10):
    """
        Kalman filter for RSSI values

        :param rssi_values: RSSI values to filter
        :param Q: Process noise covariance
        :param R: Measurement noise covariance
        :return: Filtered RSSI values

        https://www.wouterbulten.nl/posts/kalman-filters-explained-removing-noise-from-rssi-signals/
    """
    x_estime = np.array([[rssi_values[0]]])  # État initial: RSSI initial
    P = np.array([[1]])                      # Covariance initiale de l'état
    F = np.array([[1]])                      # Matrice de transition d'état
    H = np.array([[1]])                      # Matrice de mesure
    filtered_rssi = [x_estime.item()]
    
    for rssi in rssi_values[1:]:
        x_pred = F @ x_estime
        P_pred = F @ P @ F.T + Q
        
        K = P_pred @ H.T @ np.linalg.inv(H @ P_pred @ H.T + R)
        x_estime = x_pred + K @ (rssi - H @ x_pred)
        P = (np.eye(1) - K @ H) @ P_pred
        
        filtered_rssi.append(x_estime.item())
        
    return filtered_rssi
