import networkx as nx
import json
import os
import time

print("Chargement du graphe...")
gml_path = "../deliverables/week_5/cross_platform_merged.gml"

# Adjust path if run from root
if not os.path.exists(gml_path) and os.path.exists("deliverables/week_5/cross_platform_merged.gml"):
    gml_path = "deliverables/week_5/cross_platform_merged.gml"

if not os.path.exists(gml_path):
    print(f"Erreur: Le fichier {gml_path} est introuvable.")
    exit(1)

G = nx.read_gml(gml_path)
print(f"Graphe chargé: {G.number_of_nodes()} noeuds, {G.number_of_edges()} arêtes.")

print("Calcul du layout (positionnement des noeuds)... Cela peut prendre entre 5 et 15 minutes selon la puissance de votre machine.")
print("Algorithme utilisé : Spring Layout (Fruchterman-Reingold).")

start_time = time.time()
# k is optimal distance between nodes. iterations=50 is usually enough to get a decent shape while saving time
pos = nx.spring_layout(G, k=0.15, iterations=50, seed=42)

duration = time.time() - start_time
print(f"Calcul terminé en {duration:.2f} secondes !")

# Convert nodes coordinates to standard dictionary format for JSON saving
output_data = {}
for node, coords in pos.items():
    output_data[str(node)] = {"x": float(coords[0]), "y": float(coords[1])}

output_path = "deliverables/week_5/layout_positions.json"
if gml_path.startswith("../"):
    output_path = "../" + output_path

print(f"Sauvegarde des positions dans {output_path}...")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f)

print("Terminé avec succès ! Vous pouvez maintenant relancer votre Dashboard Streamlit.")
