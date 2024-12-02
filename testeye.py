import cv2
import pandas as pd

# Chemin des fichiers
video_path = "assets/Test Your Awareness.avi"
data_path = "assets/DataPOR.csv"
output_path = "assets/Output_Video_With_Points.avi"  # Nom du fichier de sortie

# Couleur et taille du point
point_color = (0, 0, 255)  # Rouge en BGR
point_radius = 30  # Rayon du point
point_thickness = 5  # -1 pour un cercle plein

# Lissage des mouvements
alpha = 0.15  # Facteur de pondération pour le lissage (0.0 = aucune transition, 1.0 = rapide)

x = 1600
y = 1150

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

# Variables pour le lissage
smoothed_x, smoothed_y = width // 2, height // 2  # Initialisation au centre

# Lire et traiter les frames
while True:
    ret, frame = cap.read()
    if not ret:
        break  # Fin de la vidéo

    # Récupérer les coordonnées actuelles
    if int(start_row) < end_row:
        raw_x = float(eye_data.iloc[int(start_row), 0]) / x * width
        raw_y = float(eye_data.iloc[int(start_row), 1]) / y * height
    else:
        raw_x, raw_y = smoothed_x, smoothed_y  # Si données épuisées, rester sur la position précédente

    # Lissage des coordonnées
    smoothed_x = int(alpha * raw_x + (1 - alpha) * smoothed_x)
    smoothed_y = int(alpha * raw_y + (1 - alpha) * smoothed_y)
    # smoothed_x = np.ones((5,5),np.float32)/25
    # swoothed_y = np.ones((5,5),np.float32)/25


    # Dessiner le point seulement si les coordonnées sont valides
    if 0 <= smoothed_x < width and 0 <= smoothed_y < height:
        #cv2.circle(frame, (smoothed_x, smoothed_y), point_radius, point_color, point_thickness)

        # Créer un masque de la même taille que la vidéo
        mask = frame.copy()
        mask[:] = 0  # Remplir le masque avec du noir

        # Dessiner le point sur le masque
        cv2.circle(mask, (smoothed_x, smoothed_y), point_radius, point_color, point_thickness)

        # Appliquer un filtre gaussien sur le masque
        mask = cv2.GaussianBlur(mask, (21, 21), 0)  # Taille du noyau et écart type ajustables

        # Ajouter le masque à la frame d'origine
        frame = cv2.addWeighted(frame, 1.0, mask, 0.5, 0)  # Fusionner avec transparence

    # Afficher la frame
        cv2.imshow("Video avec point rouge", frame)
        # Quitter si 'q' est pressé
        if cv2.waitKey(int(fps)) & 0xFF == ord('p'):
            break

    # Écrire la frame dans la vidéo de sortie
    out.write(frame)

    # Mise à jour de la ligne de données
    start_row += increment

# Libérer les ressources
cap.release()
out.release()
cv2.destroyAllWindows()

print(f"Vidéo avec effet eye tracker enregistrée sous : {output_path}")