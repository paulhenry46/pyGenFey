def generate_tikz_code(graph):
    """
    Transforme les arêtes du graphe en lignes TikZ.
    Format : source -- [edge label=particule] cible
    """
    tikz_lines = []
    
    for src, dst, particle in graph.edges:
        # On crée une ligne simple. Le style [] est vide pour l'instant.
        line = f"  {src} -- [edge label=\\({particle}\\)] {dst}"
        tikz_lines.append(line)
    
    # On assemble le tout dans l'environnement feynmandiagram
    # 'layered layout' est crucial pour que TikZ place les vertex automatiquement
    header = "\\feynmandiagram [layered layout, horizontal=inx1 to fx1] {"
    footer = "};"
    
    return header + "\n" + ",\n".join(tikz_lines) + "\n" + footer


from physics import get_info

def generate_physical_tikz(graph):
    tikz_lines = []
    
    for src, dst, particle in graph.edges:
        info = get_info(particle)
        style = info['style']
        label = info['label']
        
        # Logique des flèches pour les antifermions
        if info['is_anti'] and style == 'fermion':
            # On inverse le sens pour que la flèche pointe vers le vertex (remonte le temps)
            line = fr"  {dst} -- [{style}, edge label=\({label}\)] {src}"
        else:
            line = fr"  {src} -- [{style}, edge label=\({label}\)] {dst}"
            
        tikz_lines.append(line)
    
    header = "\\feynmandiagram [layered layout, horizontal=inx1 to fx1] {"
    footer = "};"
    
    return header + "\n" + ",\n".join(tikz_lines) + "\n" + footer


if __name__ == "__main__":
    from parser import parse_reaction
    from layout import FeynmanGraph
    reactions = ['u ubar > H > (Z0 > e+ e-) (Z0 > mu+ mu-)', 'u ubar > H > (Z0 > e+ e-) Z0', 'e+ e- > Z0 > mu+ mu-']
    for reaction in reactions:

        # 1. Analyse
        structure = parse_reaction(reaction)
        
        # 2. Topologie
        graph = FeynmanGraph(structure)
        
        # 3. Code TikZ
        tikz_final = generate_physical_tikz(graph)
        
        print(tikz_final)