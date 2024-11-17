import cv2

def charger_video(video_path):
    """
    Charge la vidéo et récupère les dimensions et le FPS.
    
    Args:
    - video_path (str): Chemin vers le fichier vidéo.
    
    Returns:
    - cap (VideoCapture): Objet de capture vidéo.
    - frame_width (int): Largeur de la vidéo.
    - frame_height (int): Hauteur de la vidéo.
    - fps (float): Frames par seconde de la vidéo.
    """
    cap = cv2.VideoCapture(video_path)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    return cap, frame_width, frame_height, fps

def initialiser_enregistrement(output_path, fps, frame_width, frame_height):
    """
    Initialise l'objet d'enregistrement vidéo.
    
    Args:
    - output_path (str): Chemin pour enregistrer la vidéo de sortie.
    - fps (float): Frames par seconde pour la vidéo.
    - frame_width (int): Largeur de la vidéo.
    - frame_height (int): Hauteur de la vidéo.
    
    Returns:
    - out (VideoWriter): Objet d'écriture vidéo.
    """
    return cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'XVID'), fps, (frame_width, frame_height))


def ajouter_point_de_regard(frame, lx, ly, rx, ry):
    """
    Ajoute un cercle rouge de taille plus grande représentant le point de regard sur une frame.
    
    Args:
    - frame (ndarray): Image de la vidéo actuelle.
    - x (int): Coordonnée X du point de regard.
    - y (int): Coordonnée Y du point de regard.
    
    Returns:
    - frame (ndarray): Frame avec le point de regard superposé.
    """
    # Couleur rouge (BGR: bleu, vert, rouge) et rayon plus grand
    cv2.circle(frame, (rx, ry), radius=50, color=(0, 0, 255), thickness=-1)  # rouge (0, 0, 255)
    cv2.circle(frame, (lx, ly), radius=50, color=(255, 0, 0), thickness=-1)  # rouge (0, 0, 255)
    return frame

