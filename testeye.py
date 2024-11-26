import cv2
import pandas as pd
import numpy as np

# Chemin des fichiers
video_path = "assets/Test Your Awareness.avi"
data_path = "assets/DataPOR.csv"
output_path = "assets/Output_Video_With_Points.avi"  # Nom du fichier de sortie

# Résolution
x = 1600
y = 1050

# Couleurs et tailles des points
current_point_color = (0, 0, 255)  # Rouge pour le point actuel
next_point_color = (0, 255, 0)  # Bleu pour le point suivant
path_point_color = (255, 0, 0)  # Vert pour les points intermédiaires
current_point_radius = 20  # Taille du point actuel
next_point_radius = 15  # Taille du point suivant
path_point_radius = 15  # Taille des points intermédiaires
point_thickness = -1

# Propriétés de l'interpolation
num_path_points = 10  # Nombre de points intermédiaires

# Charger la vidéo
cap = cv2.VideoCapture(video_path)

# Propriétés de la vidéo
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
fps = int(cap.get(cv2.CAP_PROP_FPS))
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Charger les données CSV
data = pd.read_csv(data_path, delimiter='\t', encoding='utf-8', low_memory=False)
eye_data = data.loc[1:, ["L POR X [px]", "L POR Y [px]"]]
start_row = 0
end_row = len(eye_data)
increment = end_row / frame_count

# Initialiser l'écrivain vidéo
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Codec pour AVI
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

# Variables pour le suivi
smoothed_current_x, smoothed_current_y = width // 2, height // 2  # Initialisation au centre
smoothed_next_x, smoothed_next_y = width // 2, height // 2

# Lire et traiter les frames
while True:
    ret, frame = cap.read()
    if not ret:
        break  # Fin de la vidéo

    # Récupérer les coordonnées actuelles et suivantes
    if int(start_row) < end_row - 1:
        raw_current_x = float(eye_data.iloc[int(start_row), 0]) / x * width
        raw_current_y = float(eye_data.iloc[int(start_row), 1]) / y * height
        raw_next_x = float(eye_data.iloc[int(start_row) + 2, 0]) / x * width
        raw_next_y = float(eye_data.iloc[int(start_row) + 2, 1]) / y * height
    else:
        raw_current_x, raw_current_y = smoothed_current_x, smoothed_current_y
        raw_next_x, raw_next_y = smoothed_next_x, smoothed_next_y

    # Lissage des coordonnées
    smoothed_current_x = int(0.8 * smoothed_current_x + 0.2 * raw_current_x)
    smoothed_current_y = int(0.8 * smoothed_current_y + 0.2 * raw_current_y)
    smoothed_next_x = int(0.8 * smoothed_next_x + 0.2 * raw_next_x)
    smoothed_next_y = int(0.8 * smoothed_next_y + 0.2 * raw_next_y)

    # Dessiner le point actuel
    if 0 <= smoothed_current_x < width and 0 <= smoothed_current_y < height:
         mask = frame.copy()
         mask[:] = 0

         cv2.circle(mask, (smoothed_current_x, smoothed_current_y), current_point_radius, current_point_color, point_thickness)

         mask = cv2.GaussianBlur(mask, (21, 21), 0)

         frame = cv2.addWeighted(frame, 1.0, mask, 0.5, 0)

    # Dessiner le point suivant
    if 0 <= smoothed_next_x < width and 0 <= smoothed_next_y < height:
        mask = frame.copy()
        mask[:] = 0

        cv2.circle(mask, (smoothed_next_x, smoothed_next_y), next_point_radius, next_point_color, point_thickness)

        mask = cv2.GaussianBlur(mask, (21, 21), 0)

        frame = cv2.addWeighted(frame, 1.0, mask, 0.5, 0)

    # Dessiner les points intermédiaires
    for i in range(1, num_path_points + 1):
        interp_x = int(smoothed_current_x + i * (smoothed_next_x - smoothed_current_x) / (num_path_points + 1))
        interp_y = int(smoothed_current_y + i * (smoothed_next_y - smoothed_current_y) / (num_path_points + 1))
        if 0 <= interp_x < width and 0 <= interp_y < height:
            mask = frame.copy()
            mask[:] = 0

            cv2.circle(mask, (interp_x, interp_y), path_point_radius, path_point_color, point_thickness)

            mask = cv2.GaussianBlur(mask, (21, 21), 0)

            frame = cv2.addWeighted(frame, 1.0, mask, 0.5, 0)

    # Écrire la frame dans la vidéo de sortie
    out.write(frame)

    # Mise à jour de la ligne de données
    start_row += increment

# Libérer les ressources
cap.release()
out.release()
cv2.destroyAllWindows()

print(f"Vidéo avec effet eye tracker enregistrée sous : {output_path}")
