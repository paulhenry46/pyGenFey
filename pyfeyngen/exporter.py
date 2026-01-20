from .physics import get_particle_info

class VertexManager:
    def __init__(self):
        self.count = 0
    def new_v(self):
        self.count += 1
        return f"vx{self.count}"

def to_tikz_feynman(structure):
    v_manager = VertexManager()
    lines = []

    def process_elements(current_v, elements):
        for i, item in enumerate(elements):
            if isinstance(item, list):
                # Cas d'une cascade : item est une structure complète [['Z0'], ['mu+', 'mu-']]
                # 1. On extrait le parent (le premier segment de la sous-liste)
                parent_info = get_particle_info(item[0][0])
                new_v = v_manager.new_v()
                
                # 2. On relie le vertex actuel au nouveau point de désintégration
                lines.append(fr"{current_v} -- [{parent_info['style']}, edge label=\({parent_info['label']}\)] {new_v}")
                
                # 3. On récurse pour les produits de désintégration (le reste de la liste)
                if len(item) > 1:
                    process_elements(new_v, item[1])
            else:
                # Cas d'une particule finale simple
                p = get_particle_info(item)
                node = f"f_{v_manager.count}_{i}"
                label_side = "'" if i % 2 != 0 else ""
                
                if p['is_anti'] and p['style'] == "fermion":
                    lines.append(fr"{node} -- [{p['style']}, edge label{label_side}=\({p['label']}\)] {current_v}")
                else:
                    lines.append(fr"{current_v} -- [{p['style']}, edge label{label_side}=\({p['label']}\)] {node}")

    # --- Initialisation ---
    # Pour la nouvelle structure, le premier élément est l'entrée, le reste est la cascade
    def find_inputs(struct):
        # Trouve les entrées (particules initiales)
        if isinstance(struct, list) and all(isinstance(x, str) for x in struct):
            return struct
        if isinstance(struct, list) and len(struct) > 0:
            return find_inputs(struct[0])
        return []

    v1 = v_manager.new_v() # Vertex d'entrée
    inputs = find_inputs(structure)
    for i, name in enumerate(inputs):
        p = get_particle_info(name)
        node = f"inx{i}"
        if p['is_anti'] and p['style'] == "fermion":
            lines.append(fr"{v1} -- [{p['style']}, edge label=\({p['label']}\)] {node}")
        else:
            lines.append(fr"{node} -- [{p['style']}, edge label=\({p['label']}\)] {v1}")

    # Cascade/final states
    def process_cascade(current_v, struct):
        # struct peut être une particule, une liste de particules, ou une cascade
        if isinstance(struct, str):
            p = get_particle_info(struct)
            node = f"fx{v_manager.count}x{process_cascade.fid}"
            process_cascade.fid += 1
            label_side = "'" if (process_cascade.fid % 2 == 0) else ""
            if p['is_anti'] and p['style'] == "fermion":
                lines.append(fr"{node} -- [{p['style']}, edge label{label_side}=\({p['label']}\)] {current_v}")
            else:
                lines.append(fr"{current_v} -- [{p['style']}, edge label{label_side}=\({p['label']}\)] {node}")
        elif isinstance(struct, list):
            # Si c'est une cascade de la forme [[parent], [branches...]]
            if (
                len(struct) == 2
                and isinstance(struct[0], list) and len(struct[0]) == 1 and isinstance(struct[0][0], str)
                and isinstance(struct[1], list)
            ):
                parent_info = get_particle_info(struct[0][0])
                # Si plusieurs branches, on crée un vertex intermédiaire
                if len(struct[1]) > 1:
                    parent_v = v_manager.new_v()
                    lines.append(fr"{current_v} -- [{parent_info['style']}, edge label=\({parent_info['label']}\)] {parent_v}")
                    for branch in struct[1]:
                        process_cascade(parent_v, branch)
                # Si une seule branche, on relie directement sans vertex intermédiaire
                elif len(struct[1]) == 1:
                    lines.append(fr"{current_v} -- [{parent_info['style']}, edge label=\({parent_info['label']}\)] ", end='')
                    # On continue la chaîne sur la même ligne
                    # On génère le nom du prochain vertex ou nœud final dans la branche
                    # On crée un vertex temporaire pour la suite
                    next_v = v_manager.new_v()
                    print_str = lines.pop()
                    lines.append(print_str + f"{next_v}")
                    process_cascade(next_v, struct[1][0])
            else:
                # Liste de particules ou de cascades, toutes rattachées au vertex courant
                for item in struct:
                    process_cascade(current_v, item)

    process_cascade.fid = 0

    # On traite la cascade à partir du vertex d'entrée
    process_cascade(v1, structure[1:])

    content = ",\n  ".join(lines)

    # Cherche les vertex internes générés (v1, v2, ...)
    # Détermine si la structure est strictement linéaire (pas de branches)
    def is_linear(struct):
        # Une chaîne linéaire n'a qu'un seul enfant à chaque niveau
        if isinstance(struct, str):
            return True
        if isinstance(struct, list):
            # Cascade de la forme [[parent], [enfants...]]
            if (
                len(struct) == 2
                and isinstance(struct[0], list) and len(struct[0]) == 1 and isinstance(struct[0][0], str)
                and isinstance(struct[1], list)
            ):
                return is_linear(struct[1])
            # Liste de plusieurs éléments = embranchement
            if len(struct) > 1:
                return False
            if len(struct) == 1:
                return is_linear(struct[0])
        return False

    # Toujours ajouter [horizontal=vx1 to vx2] si au moins deux vertex internes existent
    vertex_nodes = []
    for l in lines:
        parts = l.replace(',', '').split()
        for p in parts:
            if p.startswith('vx') and p[2:].isdigit() and p not in vertex_nodes:
                vertex_nodes.append(p)
    if len(vertex_nodes) >= 2:
        horizontal = f"[horizontal={vertex_nodes[0]} to {vertex_nodes[1]}]"
    else:
        horizontal = ""

    return fr"\feynmandiagram {horizontal} {{" + "\n  " + content + "\n};"