import cv2
import time
import datetime
import threading
from ultralytics import YOLO

# --- CONFIGURACIÓN DEL SERVIDOR ---
RTSP_URL = "rtsp://Nico:Nico2025@190.102.229.163:8554/cam/realmonitor?channel=6&subtype=0"
MODEL_PATH = "fuego-seg.pt"
CONFIDENCE_THRESHOLD = 0.5

# Configuración de Alertas
LOG_COOLDOWN = 3.0  # Segundos de espera entre alertas repetidas para no saturar la consola
HEARTBEAT_INTERVAL = 60.0 # Cada cuántos segundos avisar que el sistema sigue vivo

# Etiquetas (Solo para el texto del log)
LABELS = {
    0: "FUEGO 🔥",
    1: "HUMO ☁️"
}

class VideoStream:
    """
    Clase optimizada para lectura de buffer RTSP en segundo plano.
    """
    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)
        if not self.stream.isOpened():
            print(f"[{datetime.datetime.now()}] ❌ ERROR CRÍTICO: No se puede conectar a la cámara.")
            self.stopped = True
        else:
            self.stopped = False
            (self.grabbed, self.frame) = self.stream.read()

    def start(self):
        threading.Thread(target=self.update, args=(), daemon=True).start()
        return self

    def update(self):
        while not self.stopped:
            if not self.grabbed:
                self.stop()
            else:
                (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True
        self.stream.release()

def run_server_monitor():
    print(f"--- INICIANDO SERVIDOR DE DETECCIÓN ---")
    print(f"📍 Modelo: {MODEL_PATH}")
    print(f"📍 Cámara: {RTSP_URL}")
    
    # 1. Cargar Modelo
    try:
        model = YOLO(MODEL_PATH)
    except Exception as e:
        print(f"❌ Error al cargar el modelo: {e}")
        return

    # 2. Iniciar Stream
    video_stream = VideoStream(RTSP_URL).start()
    time.sleep(2.0) # Esperar a que estabilice

    if video_stream.stopped:
        print("❌ El servicio se detuvo por error de conexión.")
        return

    print(f"✅ [{datetime.datetime.now()}] SISTEMA EN LÍNEA Y VIGILANDO.")

    # Variables de control
    last_alert_time = {} # Diccionario para cooldown por clase
    last_heartbeat = time.time()

    try:
        while True:
            # Obtener frame actual
            frame = video_stream.read()
            if frame is None:
                print("⚠️ Advertencia: Frame vacío, reintentando...")
                time.sleep(1)
                continue

            # --- INFERENCIA ---
            # verbose=False evita que YOLO imprima basura en la consola en cada frame
            results = model.predict(source=frame, conf=CONFIDENCE_THRESHOLD, imgsz=640, verbose=False)
            
            # Revisar detecciones
            # Accedemos directo a las cajas (boxes) porque es más rápido que procesar máscaras
            # si solo queremos saber "QUÉ" hay y no "DÓNDE EXACTAMENTE".
            detected_classes = results[0].boxes.cls.cpu().numpy()
            confidences = results[0].boxes.conf.cpu().numpy()
            
            current_time = time.time()

            # Si hay detecciones
            if len(detected_classes) > 0:
                for i, class_id in enumerate(detected_classes):
                    c_id = int(class_id)
                    conf = confidences[i]

                    # Verificar Cooldown para esta clase específica
                    if current_time - last_alert_time.get(c_id, 0) > LOG_COOLDOWN:
                        
                        # --- ENVIAR MENSAJE POR CONSOLA ---
                        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        label_text = LABELS.get(c_id, f"Clase {c_id}")
                        
                        # Mensaje estructurado
                        print(f"🚨 [ALERTA] {timestamp} | Detectado: {label_text} | Confianza: {conf:.2f}")
                        
                        # Actualizar tiempo de última alerta
                        last_alert_time[c_id] = current_time

            # Heartbeat (Latido) para saber que el script no murió
            if current_time - last_heartbeat > HEARTBEAT_INTERVAL:
                print(f"ℹ️ [{datetime.datetime.now().strftime('%H:%M:%S')}] Estado: Sistema operativo y escaneando...")
                last_heartbeat = current_time

            # Pequeño sleep para no quemar la CPU innecesariamente en bucles vacíos
            # (El stream de video limita los FPS naturalmente, pero esto ayuda)
            time.sleep(0.01)

    except KeyboardInterrupt:
        print("\n🛑 Deteniendo servidor manualmente...")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
    finally:
        video_stream.stop()
        print("✅ Servicio detenido correctamente.")

if __name__ == "__main__":
    run_server_monitor()