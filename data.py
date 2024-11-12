import pandas as pd

def charger_donnees(fichier_path):
    """
    Charge les données de point de regard depuis un fichier .txt.

    Args:
    - fichier_path (str): Chemin vers le fichier .txt contenant les données.

    Returns:
    - DataFrame contenant les données de point de regard.
    """
    try:
        # Charger le fichier avec un délimiteur tabulation, en désactivant le mode de faible mémoire
        data = pd.read_csv(fichier_path, delimiter='\t', encoding='utf-8', low_memory=True)
        
        # Forcer les colonnes pertinentes à être de type float pour éviter les erreurs
        cols_to_convert = ['L POR X [px]', 'L POR Y [px]', 'R POR X [px]', 'R POR Y [px]', 'Time']
        for col in cols_to_convert:
            data[col] = pd.to_numeric(data[col], errors='coerce')
        
        return data
    except Exception as e:
        print(f"Erreur lors du chargement des données : {e}")
        return None
