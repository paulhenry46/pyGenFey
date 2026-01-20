
class VertexManager:
    """
    Gère la création d'identifiants uniques pour les points d'interaction (vertex).
    C'est crucial pour les diagrammes en cascade où chaque désintégration 
    nécessite un nouveau point d'ancrage.
    """
    def __init__(self):
        self.count = 0

    def new_v(self):
        """Génère et retourne un nom de vertex unique (v1, v2, v3...)."""
        self.count += 1
        return f"v{self.count}"

    def reset(self):
        """Réinitialise le compteur (utile pour générer plusieurs diagrammes)."""
        self.count = 0

def calculate_step_spacing(num_particles):
    """
    Optionnel : Calcule des paramètres d'espacement si l'on souhaite 
    forcer des angles spécifiques dans TikZ.
    """
    if num_particles <= 1:
        return 0
    return 360 / num_particles