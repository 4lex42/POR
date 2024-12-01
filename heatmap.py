import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Charger le fichier CSV avec le bon séparateur
file_path = 'assets/DataPOR.csv'
df = pd.read_csv(file_path, sep="\t")

# Convertir les colonnes en valeurs numériques (forcer les erreurs à NaN)
df["L POR X [px]"] = pd.to_numeric(df["L POR X [px]"], errors='coerce')
df["L POR Y [px]"] = pd.to_numeric(df["L POR Y [px]"], errors='coerce')

# Supprimer les lignes avec des NaN dans les colonnes pertinentes
df_cleaned = df.dropna(subset=["L POR X [px]", "L POR Y [px]"])
df_cleaned = df_cleaned[(df_cleaned["L POR X [px]"] != 0) | (df_cleaned["L POR Y [px]"] != 0)]

# Extraire les colonnes nécessaires
x_values = df_cleaned["L POR X [px]"]
y_values = df_cleaned["L POR Y [px]"]

# Définir la résolution de la heatmap
x_bins = 50  # Nombre de bins pour l'axe X
y_bins = 50  # Nombre de bins pour l'axe Y

# Créer un histogramme 2D avec une plage explicite pour les axes
x_range = (0, 1920)  # Plage pour l'axe X
y_range = (0, 1080)  # Plage pour l'axe Y
heatmap, xedges, yedges = np.histogram2d(x_values, y_values, bins=[x_bins, y_bins], range=[x_range, y_range])

# Transformer en DataFrame pour l'utiliser avec seaborn
heatmap_df = pd.DataFrame(heatmap)

# Dessiner la heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(heatmap_df, cmap="Reds", cbar=True, vmax=100)

# Ajuster les étiquettes des axes pour correspondre à la plage choisie
plt.title("Heatmap des Points de Regards")
plt.xlabel("Position X")
plt.ylabel("Position Y")

# Ajouter des ticks correspondant aux limites des bins
plt.xticks(np.linspace(0, x_bins, num=6), labels=np.linspace(0, 1920, num=6, dtype=int))
plt.yticks(np.linspace(0, y_bins, num=6), labels=np.linspace(0, 1080, num=6, dtype=int))

plt.show()
