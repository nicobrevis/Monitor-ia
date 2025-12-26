# 🔥 Servidor de Detección de Fuego y Humo (Headless Edition)

Este repositorio contiene un script optimizado en Python (`fuego-server.py`) diseñado para ejecutarse en servidores Linux/Windows sin interfaz gráfica (Headless). Su función es monitorear flujos de video RTSP en tiempo real, detectar incidencias de fuego o humo utilizando Inteligencia Artificial (YOLOv8) y reportar alertas a través de la consola del sistema o logs.

---

## 📋 Características Principales

* **Modo Headless (Sin GUI):** No requiere monitor ni entorno de escritorio. No genera ventanas emergentes (`cv2.imshow`), lo que reduce drásticamente el consumo de CPU/GPU.
* **Lectura Asíncrona (Threading):** Implementa un hilo independiente (`VideoStream`) para la captura de video, evitando que el procesamiento de la IA congele la lectura de la cámara (latencia cero).
* **Logs Inteligentes:** Sistema de alertas con "Enfriamiento" (Cooldown) para evitar saturar el disco o la consola con mensajes repetitivos.
* **Heartbeat (Latido):** Emite una señal de vida cada 60 segundos para confirmar que el sistema sigue operativo incluso si no hay detecciones.

---

## ⚙️ Requisitos e Instalación

### Prerrequisitos
* Python 3.8 o superior.
* Entorno Linux (Ubuntu/Debian) o Windows Server.
* Conexión de red a la cámara CCTV.

### Instalación de Dependencias
Para un entorno de servidor, se recomienda usar `opencv-python-headless` para evitar errores de librerías gráficas faltantes.

```bash
pip install ultralytics
pip install opencv-python-headless
