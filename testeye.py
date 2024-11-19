import cv2
import pandas as pd

# Chemin des fichiers
video_path = "assets/Test Your Awareness.avi"
data_path = "assets/DataPOR.csv"
output_path = "assets/Output_Video_With_Points.avi"  # Nom du fichier de sortie

# Coordonnées du point rouge
point_color = (0, 0, 255)  # Rouge en BGR
point_radius = 5  # Rayon du point
point_thickness = -1  # -1 pour un cercle plein

# Charger la vidéo
cap = cv2.VideoCapture(video_path)

# Obtenir les propriétés de la vidéo
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
fps = int(cap.get(cv2.CAP_PROP_FPS))
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Affichage des propriétés
print(f"Résolution : {width} x {height}")
print(f"{fps} images/seconde")
print(f"Nombre total de frames : {frame_count}")

# Charger le fichier CSV avec un délimiteur tabulation
data = pd.read_csv(data_path, delimiter='\t', encoding='utf-8', low_memory=False)

# Extraire les colonnes des coordonnées X et Y de l'œil gauche
eye_data = data.loc[1:, ["L POR X [px]", "L POR Y [px]"]]
start_row = 0
end_row = len(eye_data)
increment = end_row / frame_count  # Nombre de lignes à sauter pour chaque frame

# Vérification si la vidéo s'ouvre correctement
if not cap.isOpened():
    print("Erreur : Impossible de charger la vidéo.")
    exit()

# Initialiser l'écrivain vidéo
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Codec pour AVI
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

# Lire et traiter les frames
while True:
    ret, frame = cap.read()
    if not ret:
        break  # Fin de la vidéo

    # Calculer les coordonnées X et Y de l'œil
    if int(start_row) < end_row:
        eye_x = int(float(eye_data.iloc[int(start_row), 0]) / 1920 * width)
        eye_y = int(float(eye_data.iloc[int(start_row), 1]) / 1080 * height)
    else:
        eye_x, eye_y = -1, -1  # Valeurs invalides si les données sont épuisées

    # Dessiner le point uniquement si les coordonnées sont valides
    if 0 <= eye_x < width and 0 <= eye_y < height:
        cv2.circle(frame, (eye_x, eye_y), point_radius, point_color, point_thickness)

    # Écrire la frame dans le fichier de sortie
    out.write(frame)

    start_row += increment

# Libérer les ressources
cap.release()
out.release()
cv2.destroyAllWindows()

print(f"Vidéo traitée enregistrée sous : {output_path}")
