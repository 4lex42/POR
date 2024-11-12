from data import charger_donnees
from video import charger_video, initialiser_enregistrement, ajouter_point_de_regard

def main():
    # Charger les données de point de regard
    fichier_donnees = 'assets/Test Your Awareness eyes data.txt'
    data = charger_donnees(fichier_donnees)
    print(data)

    if data is None:
        print("Erreur lors du chargement des données. Vérifiez le fichier et réessayez.")
        return

    # Filtrer pour ne garder que les lignes contenant des données de type 'SMP'
    data = data[data['Type'] == 'SMP']

    # Charger la vidéo
    video_path = 'assets/Test Your Awareness.avi'
    cap, frame_width, frame_height, fps = charger_video(video_path)

    if not cap.isOpened():
        print("Erreur lors du chargement de la vidéo. Vérifiez le chemin et réessayez.")
        return

    # Initialiser l'enregistrement de la vidéo avec les annotations
    output_path = 'assets/Output_Video_With_Points.avi'
    out = initialiser_enregistrement(output_path, fps, frame_width, frame_height)

    frame_idx = 0

    # Parcourir chaque frame de la vidéo
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Calculer le temps de la frame actuelle en millisecondes
        current_time = (frame_idx / fps) * 1000

        # Trouver les données les plus proches du temps actuel
        row = data.iloc[(data['Time'] - current_time).abs().argsort()[:1]]
        
        # Vérifier si les coordonnées sont bien présentes
        if not row.empty:
            # Obtenir les coordonnées X et Y du regard
            x = int(row['L POR X [px]'].values[0])  # ou 'R POR X [px]' selon le côté que tu veux suivre
            y = int(row['L POR Y [px]'].values[0])  # ou 'R POR Y [px]'

            # Ajouter le point de regard sur la frame
            frame = ajouter_point_de_regard(frame, x, y)

        # Ajouter la frame annotée à la vidéo de sortie
        out.write(frame)
        
        frame_idx += 1

    # Libérer les ressources
    cap.release()
    out.release()
    print("Traitement terminé. La vidéo avec les points de regard a été enregistrée.")

if __name__ == "__main__":
    main()