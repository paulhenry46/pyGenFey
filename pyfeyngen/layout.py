class FeynmanGraph:
    def __init__(self, structure):
        self.nodes = []      
        self.edges = []      
        self.v_count = 0
        self.in_count = 0
        self.f_count = 0
        # Mémoire des ancres : { "nom": [{"vertex": "vx1", "particle": "gamma"}, ...] }
        self.anchor_points = {} 
        
        self.build_graph(structure)

    def new_v(self):
        self.v_count += 1
        return f"vx{self.v_count}"

    def new_in(self):
        self.in_count += 1
        return f"inx{self.in_count}"

    def new_f(self):
        self.f_count += 1
        return f"fx{self.f_count}"

    def build_graph(self, structure):
        v_start = self.new_v()
        
        # On filtre pour ne garder que les noms de particules (str)
        # u ubar @debut -> ['u', 'ubar']
        in_particles = [p for p in structure[0] if isinstance(p, str)]
        
        # On enregistre les ancres d'entrée sur le vertex de départ
        in_anchors = [p for p in structure[0] if isinstance(p, dict)]
        for a in in_anchors:
            self._register_anchor(v_start, a)

        for p in in_particles:
            in_node = self.new_in()
            self.edges.append((in_node, v_start, p))
        
        self._process_steps(v_start, structure[1:])
        self._connect_anchors()
        

    def _process_steps(self, current_v, steps):
        if not steps: return
        step = steps[0]

        # On sépare les ancres des particules réelles dans cette étape
        particles = [item for item in step if isinstance(item, str) or isinstance(item, list)]
        anchors = [item for item in step if isinstance(item, dict) and 'anchor' in item]

        # On enregistre les ancres sur le vertex actuel
        for a in anchors:
            self._register_anchor(current_v, a)

        # Si l'étape n'a plus de particules (seulement des ancres), on passe à la suite
        if not particles:
            self._process_steps(current_v, steps[1:])
            return

        # --- RESTE DE LA LOGIQUE AVEC 'particles' au lieu de 'step' ---
        if len(particles) == 1 and not isinstance(particles[0], list):
            v_next = self.new_v()
            self.edges.append((current_v, v_next, particles[0]))
            self._process_steps(v_next, steps[1:])
        else:
            for item in particles:
                if isinstance(item, list):
                    v_decay = self.new_v()
                    # On cherche la particule parente dans la cascade
                    p_name = next((t for t in item[0] if isinstance(t, str)), "unknown")
                    # On enregistre les ancres présentes dans la définition de la cascade
                    for t in item[0]:
                        if isinstance(t, dict) and 'anchor' in t:
                            self._register_anchor(v_decay, t)
                    
                    self.edges.append((current_v, v_decay, p_name))
                    self._process_steps(v_decay, item[1:])
                else:
                    f_node = self.new_f()
                    self.edges.append((current_v, f_node, item))

    def _register_anchor(self, vertex, anchor_dict):
        """Enregistre un vertex pour une ancre donnée."""
        name = anchor_dict['anchor']
        if name not in self.anchor_points:
            self.anchor_points[name] = []
        self.anchor_points[name].append({
            'vertex': vertex,
            'particle': anchor_dict.get('particle')
        })

    def _connect_anchors(self):
        """Relie les points marqués par les mêmes ancres à la fin."""
        for name, points in self.anchor_points.items():
            if len(points) >= 2:
                # On relie les points deux à deux
                for i in range(len(points) - 1):
                    src = points[i]['vertex']
                    dst = points[i+1]['vertex']
                    # On utilise la particule définie dans l'ancre (ou photon par défaut)
                    p_name = points[i]['particle'] or "gamma"
                    self.edges.append((src, dst, p_name))

if __name__ == "__main__":
    # Simulation d'une structure parsée complexe : 
    # u ubar > H > (Z0 > e+ e-) (Z0 > mu+ mu-)
    mock_structure = [
        ['u', 'ubar'],                                     # Entrées
        ['H'],                                             # Étape 1
        [                                                  # Étape 2 (Branchement)
            [['Z0'], ['e+', 'e-']],                        # Cascade 1
            [['Z0'], ['mu+', 'mu-']]                       # Cascade 2
        ]
    ]

    mock_structure =  [['H'], [[['Z0'], ['e+', 'e-']], 'Z0']]
    mock_structure = [['e+', 'e-'], ['Z0'], ['mu+', 'mu-']]

    print("--- TEST DU GENERATEUR DE GRAPHE ---")
    graph = FeynmanGraph(mock_structure)

    print(f"\nNoeuds créés : {graph.v_count} vertex, {graph.in_count} entrées, {graph.f_count} sorties.")
    
    print("\nListe des connexions (Edges) :")
    print(f"{'Source':<10} | {'Cible':<10} | {'Particule':<10}")
    print("-" * 35)
    for src, dst, particle in graph.edges:
        print(f"{src:<10} | {dst:<10} | {particle:<10}")

    