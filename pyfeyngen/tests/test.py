if __name__ == "__main__":
    from parser import parse_reaction
    from exporter import generate_physical_tikz
    from layout import FeynmanGraph
    reactions = [
                 'u ubar > H > (Z0 > e+ e-) (Z0 > mu+ mu-)', 
                 'u ubar > H > (Z0 > e+ e-) Z0', 
                 'e+ e- > Z0 > mu+ mu-'
                 ]
    for reaction in reactions:

        # 1. Analyse
        structure = parse_reaction(reaction)
        
        # 2. Topologie
        graph = FeynmanGraph(structure)
        
        # 3. Code TikZ
        tikz_final = generate_physical_tikz(graph)
        
        print(tikz_final)