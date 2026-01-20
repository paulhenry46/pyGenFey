from .physics import get_info

from .physics import get_info

from .physics import get_info

def generate_physical_tikz(graph):
    tikz_lines = []
    vertex_usage = {}
    # Ensemble pour suivre les vertex déjà déclarés avec un style
    styled_vertices = set()

    # 1. FILTRAGE ET COMPTAGE PRÉALABLE
    path_totals = {}
    valid_edges = []
    for edge in graph.edges:
        src, dst, particle = edge
        if isinstance(particle, str):
            valid_edges.append(edge)
            path_id = tuple(sorted((src, dst)))
            path_totals[path_id] = path_totals.get(path_id, 0) + 1

    path_current_count = {}

    # 2. GÉNÉRATION DES LIGNES TIKZ
    for src, dst, particle in valid_edges:
        info = get_info(particle)
        style = info['style']
        label = info['label']
        path_id = tuple(sorted((src, dst)))
        
        # --- Gestion des styles de vertex (Injection unique) ---
        src_attr = ""
        if src in graph.vertex_styles and src not in styled_vertices:
            src_attr = f"[{graph.vertex_styles[src]}]"
            styled_vertices.add(src)
            
        dst_attr = ""
        if dst in graph.vertex_styles and dst not in styled_vertices:
            dst_attr = f"[{graph.vertex_styles[dst]}]"
            styled_vertices.add(dst)
        
        # --- Gestion du Multi-Bending ---
        bend_style = ""
        total_lines = path_totals[path_id]
        if total_lines > 1:
            idx = path_current_count.get(path_id, 0)
            path_current_count[path_id] = idx + 1
            max_bend = 50 
            step = (max_bend * 2) / (total_lines - 1)
            angle = -max_bend + (step * idx)
            if info['is_anti'] and style == 'fermion': angle = -angle
            if abs(angle) > 0.1:
                side = "left" if angle > 0 else "right"
                bend_style = f"bend {side}={abs(int(angle))}"
        
        # --- Gestion du Label Side ---
        count_usage = vertex_usage.get(src, 0)
        label_side = "'" if count_usage % 2 != 0 else "" 
        vertex_usage[src] = count_usage + 1
        
        # --- Construction des options de l'arête ---
        label_cmd = fr"edge label{label_side}=\({label}\)" if label else ""
        options = [style]
        if bend_style: options.append(bend_style)
        if label_cmd: options.append(label_cmd)
        options_str = ", ".join(options)

        # --- Assemblage final (Syntaxe vertex[style] unique) ---
        if info['is_anti'] and style == 'fermion':
            line = fr"  {dst}{dst_attr} -- [{options_str}] {src}{src_attr}"
        else:
            line = fr"  {src}{src_attr} -- [{options_str}] {dst}{dst_attr}"
            
        tikz_lines.append(line)
    
    header = "\\feynmandiagram [layered layout, horizontal=inx1 to fx1] {"
    footer = "};"
    
    return header + "\n" + ",\n".join(tikz_lines) + "\n" + footer

if __name__ == "__main__":
    from .parser import parse_reaction
    from .layout import FeynmanGraph
    
    # Test avec une réaction à ancre (Échange de photon entre deux branches)
    reactions = [
        'u ubar > H > (Z0 @link > e+ e-) (Z0 @link > mu+ mu-)',
        'e- > @box:gamma e- > @box'
    ]
    
    for reaction in reactions:
        print(f"\n--- Test: {reaction} ---")
        structure = parse_reaction(reaction)
        graph = FeynmanGraph(structure)
        print(generate_physical_tikz(graph))