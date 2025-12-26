# 🔥 Sistema de Detección de Fuego y Humo con IA (YOLOv8)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![YOLOv8](https://img.shields.io/badge/AI-YOLOv8-green)
![OpenCV](https://img.shields.io/badge/Computer_Vision-OpenCV-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

Este proyecto es una solución de videovigilancia inteligente diseñada para detectar **incendios y humo** en tiempo real utilizando modelos de segmentación **YOLOv8**.

El sistema está optimizado para funcionar en dos entornos:
1.  **Modo Servidor (Headless):** Ejecución eficiente en servidores Linux/Windows sin interfaz gráfica, con alertas por consola y logs.
2.  **Modo Visual (Desktop):** Panel de control gráfico con segmentación de instancias, dashboard de confianza y grabación de video.

---

## 🚀 Características

* **Detección Dual:** Identificación simultánea de Fuego (Clase 0) y Humo (Clase 1).
* **Streaming RTSP Asíncrono:** Implementación de hilos (threading) para evitar latencia en cámaras CCTV.
* **Optimización de Recursos:** Versión dedicada para servidores que elimina el renderizado gráfico para maximizar FPS.
* **Sistema de Logs Inteligente:**
    * "Enfriamiento" (Cooldown) de alertas para evitar spam en la consola.
    * "Heartbeat" (Latido) para monitorear la salud del sistema.
* **Grabación de Evidencia:** Generación automática de reportes en video (en la versión visual).

---

## 📋 Requisitos Previos

* **Hardware:**
    * CPU Multicore o GPU NVIDIA (Recomendada con CUDA para inferencia rápida).
    * Cámara IP con soporte RTSP o archivos de video `.mp4`.
* **Software:**
    * Python 3.8 o superior.

---

## 🛠️ Instalación

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/TU_USUARIO/fire-detection-yolo.git](https://github.com/TU_USUARIO/fire-detection-yolo.git)
    cd fire-detection-yolo
    ```

2.  **Crear un entorno virtual (Opcional pero recomendado):**
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # Linux/Mac
    source .venv/bin/activate
    ```

3.  **Instalar dependencias:**
    
    *Para ejecutar en Servidor (Headless):*
    ```bash
    pip install -r requirements.txt
    ```
    *(Asegúrate de que `requirements.txt` contenga `opencv-python-headless`)*

    *Para ejecutar en Desktop (Con ventanas):*
    ```bash
    pip install ultralytics opencv-python numpy
    ```

---

## ⚙️ Configuración

Edita las variables principales al inicio de los scripts (`fuego-server.py` o `fuego-seg.py`):

```python
# URL de tu cámara CCTV
RTSP_URL = "rtsp://usuario:contraseña@192.168.1.X:554/stream"

# Ruta del modelo entrenado
MODEL_PATH = "fuego-seg.pt"

# Sensibilidad de la detección (0.0 a 1.0)
CONFIDENCE_THRESHOLD = 0.5
