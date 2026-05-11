import cv2
from ultralytics import YOLO

# Charger le modèle YOLO pré-entraîné (version nano, la plus rapide)
model = YOLO("yolov8n.pt")

video_path = "video.mp4"
cap = cv2.VideoCapture(video_path)
print(cap.isOpened())  

# Récupérer les infos de la vidéo
fps = cap.get(cv2.CAP_PROP_FPS)                        # images par seconde
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # hauteur en pixels
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))    # largeur en pixels

# --- CONFIG ---
BOTTOM_LINE = int(frame_height * 0.75)  # ligne invisible en bas (75% de la hauteur)
PROXIMITY_PX = 50                        # à 50px de la ligne du bas → rouge
PROXIMITY_PX_SIDES = 5                   # à 5px du bord gauche/droit → rouge
FLASH_DURATION = int(fps * 0.6)          # durée du flash rouge en frames (~0.6 sec)

vehicles = {}  # dictionnaire final : stocke le vrai pic (basé sur max area) de chaque véhicule
live = {}      # dictionnaire temps réel : suit chaque véhicule pendant la vidéo

frame_number = 0  # compteur de frames

while True:
    ret, frame = cap.read()  # lire la frame suivante
    if not ret:              # plus de frames → fin de la vidéo
        break

    # Détection + tracking : YOLO détecte les objets et leur assigne un ID persistant
    results = model.track(frame, persist=True)
    boxes = results[0].boxes  # récupérer les bounding boxes détectées

    if boxes.id is not None:  # si au moins un objet est détecté avec un ID
        for box, track_id in zip(boxes.xyxy, boxes.id):  # parcourir chaque détection
            x1, y1, x2, y2 = map(int, box)  # coordonnées de la bounding box (coins haut-gauche et bas-droit)
            area = (x2 - x1) * (y2 - y1)    # surface en pixels² → plus c'est grand, plus c'est proche
            track_id = int(track_id)          # ID unique du véhicule suivi

            # Première apparition de ce véhicule → initialiser ses données
            if track_id not in live:
                live[track_id] = {
                    "max_area": area,                      # plus grande area vue jusqu'ici
                    "peak_frame": frame_number,            # frame où le max area a été atteint
                    "peak_position": (x1, y1, x2, y2),    # position à ce moment
                    "crossed": False,                      # a-t-il traversé une ligne ?
                    "flash_until": -1                       # jusqu'à quelle frame afficher le rouge
                }
            else:
                t = live[track_id]
                # Si l'area actuelle est plus grande que le max enregistré → mettre à jour
                if area > t["max_area"]:
                    t["max_area"] = area
                    t["peak_frame"] = frame_number
                    t["peak_position"] = (x1, y1, x2, y2)

            t = live[track_id]

            # --- VISUEL : vérifier la proximité aux lignes invisibles ---

            # Proche de la ligne du bas ? (y2 = bas de la box)
            near_bottom = abs(y2 - BOTTOM_LINE) < PROXIMITY_PX and y2 >= BOTTOM_LINE - PROXIMITY_PX

            # Proche du bord gauche ? (x1 = côté gauche de la box)
            near_left = x1 < PROXIMITY_PX_SIDES

            # Proche du bord droit ? (x2 = côté droit de la box)
            near_right = x2 > frame_width - PROXIMITY_PX_SIDES

            # Rouge si proche d'au moins une des 3 lignes
            is_near = near_bottom or near_left or near_right

            # La box a-t-elle traversé une ligne ?
            crossed_now = y2 >= BOTTOM_LINE or x1 <= 0 or x2 >= frame_width

            # Première traversée → confirmer, déclencher le flash, sauvegarder les données
            if not t["crossed"] and crossed_now:
                t["crossed"] = True                            # marquer comme traversé (une seule fois)
                t["flash_until"] = frame_number + FLASH_DURATION  # flash rouge pendant X frames
                # Sauvegarder les données EXACTES basées sur l'area (pas sur la ligne)
                vehicles[track_id] = {
                    "max_area": t["max_area"],                 # la vraie plus grande area
                    "timestamp": t["peak_frame"] / fps,        # le vrai timestamp du pic
                    "frame": t["peak_frame"],                  # la vraie frame du pic
                    "position": t["peak_position"]             # la vraie position du pic
                }

            # Est-ce qu'on est encore dans la durée du flash ?
            is_flash = t["crossed"] and frame_number <= t["flash_until"]

            # --- COULEUR : rouge si proche ou flash, vert sinon ---
            if is_flash or is_near:
                color = (0, 0, 255)   # rouge (BGR)
                thickness = 3
                label = f"Car {track_id} CLOSEST!"
            else:
                color = (0, 255, 0)   # vert (BGR)
                thickness = 2
                label = f"Car {track_id}"

            # Dessiner le rectangle autour du véhicule
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)

            # Dessiner le texte au dessus du rectangle
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    # Afficher la frame à l'écran
    cv2.imshow("Vehicle Tracking", frame)

    # Quitter si on appuie sur 'q'
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

    frame_number += 1  # passer à la frame suivante

# Libérer la vidéo et fermer les fenêtres
cap.release()
cv2.destroyAllWindows()

# --- RÉSULTATS FINAUX ---
# Ces données sont basées sur le MAX AREA (le vrai moment le plus proche)
# PAS sur la ligne d'arrivée (qui est juste pour le visuel)
print("\n=== Closest Moments ===")
for car_id, data in vehicles.items():
    print(f"""
Car ID: {car_id}
Closest Time: {data['timestamp']:.2f} sec
Frame: {data['frame']}
Max Area: {data['max_area']}
Position: {data['position']}
""")