from data import charger_donnees
from video import charger_video, initialiser_enregistrement, ajouter_point_de_regard

def main():
    # Charger les données de point de regard
    fichier_donnees = 'assets/DataPOR.csv'
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

        row = data.iloc[frame_idx]
        
        # Calculer le temps de la frame actuelle en millisecondes
        #current_time = (frame_idx / fps) * 1000

        # Trouver les données les plus proches du temps actuel
        #row = data.iloc[(data['Time'] - current_time).abs().argsort()[:1]]

        frame_idx += 20
        if frame_idx > 33976:
            frame_idx = 33976
        
        print(frame_idx)
        
        # Vérifier si les coordonnées sont bien présentes
        if not row.empty:
            # Obtenir les coordonnées X et Y du regard
            lx = int(data.iloc[frame_idx, 21])  # ou 'R POR X [px]' selon le côté que tu veux suivre
            ly = int(data.iloc[frame_idx, 22])  # ou 'R POR Y [px]'

            rx = int(data.iloc[frame_idx, 23])
            ry = int(data.iloc[frame_idx, 24])

            # Ajouter le point de regard sur la frame
            frame = ajouter_point_de_regard(frame, lx, ly, rx, ry)

        # Ajouter la frame annotée à la vidéo de sortie
        out.write(frame)

    # Libérer les ressources
    cap.release()
    out.release()
    print("Traitement terminé. La vidéo avec les points de regard a été enregistrée.")

if __name__ == "__main__":
    main()