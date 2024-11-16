import cv2
import pandas as pd

# Chemin des fichiers
video_path = "assets/Test Your Awareness.avi"
data_path = "assets/DataPOR.csv"

# Coordonnées du point rouge
point_x = 480  # Exemple, à ajuster
point_y = 360  # Exemple, à ajuster

# Couleur et taille du point
point_color = (0, 0, 255)  # Rouge en BGR
point_radius = 5  # Rayon du point
point_thickness = -1  # -1 pour un cercle plein

# Charger la vidéo
cap = cv2.VideoCapture(video_path)

# hauteur et largeur du fichier vidéo en px 
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
# Affichage de la résolution du fichier vidéo
print(f"resolution {width} x {height}")

# Nombre d'images par seconde du fichier vidéo
fps = cap.get(cv2.CAP_PROP_FPS)
# Affichage du nombre d'images par seconde du fichier vidéo
print(f"{fps} images/seconde")

# Nombre d'images au total et durée de la vidéo
frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
duration = frame_count/fps
# Affichage de la durée et du nombre de frame
print(f"{duration} secondes")
print(f"nombre de frames de la video : {frame_count}")

# Charger le fichier avec un délimiteur tabulation, en désactivant le mode de faible mémoire
data = pd.read_csv(data_path, delimiter='\t', encoding='utf-8', low_memory=False)
# Nombre de lignes totales du fichier DataPOR
row_count = len(data)
print(f"nombre de lignes csv : {row_count}")

# Colonnes X et Y de l'oeil gauche sauf la première ligne car elle est NaN
eye_data = data.loc[1:,["L POR X [px]", "L POR Y [px]"]]
start_row = 0
end_row = len(eye_data)
# Affichage des datas des colonnes
print(eye_data)
print(f"Nombre de colonnes a traiter {end_row}")
print(f"premiere ligne de L POR X :{eye_data.iloc[0,0]}")

# Nombre de lignes à sauter pour avoir le numéro de la prochaine ligne à traiter
increment = end_row/frame_count
print(f"Ajouter : {increment} pour connaitre la prochaine ligne a traiter")

# Vérifier si la vidéo s'ouvre correctement
if not cap.isOpened():
    print("Erreur : Impossible de charger la vidéo.")
    exit()

# Lire et afficher les frames
while True:
    ret, frame = cap.read()

    if not ret:
        break  # Fin de la vidéo

    # Les coordonnées X et Y de l'oeil
    eye_x = int(float((eye_data.iloc[int(start_row),0])) / 1920 * 980)
    eye_y = int(float((eye_data.iloc[int(start_row),1])) / 1080 * 720)
    #print(f"x = {eye_x} et y = {eye_y}")

    # Dessiner le point sur la frame
    cv2.circle(frame, (eye_x, eye_y), point_radius, point_color, point_thickness)

    # Afficher la frame
    cv2.imshow("Video avec point rouge", frame)

    # Quitter si 'q' est pressé
    if cv2.waitKey(int(fps)) & 0xFF == ord('p'):
        break

    start_row += increment

# Libérer les ressources
cap.release()
cv2.destroyAllWindows()