import pyfeyngen.parser as parser
import pyfeyngen.exporter as exporter

def main():
    print("--- PyFeynGen CLI ---")
    
    # 1. Définition de la réaction
    # Teste une cascade complexe : 
    # Le Higgs se désintègre en deux Z, et l'un des Z se désintègre en muons.
    reaction = "H > (Z0 > mu+ mu-) Z0"
   # reaction = "e+ e- > Z0 > mu+ mu-"
    reaction = "u ubar > H > (Z0 > e+ e-) (Z0 > mu+ mu-)"
    
    print(f"Analyse de la réaction : {reaction}")

    try:
        # 2. Parsing récursif (gère les parenthèses)
        structure = parser.parse_reaction(reaction)
        print("\nStructure analysée :\n", structure)
        
        # 3. Génération du code TikZ
        # L'exporter utilise maintenant le VertexManager interne
        tikz_code = exporter.to_tikz_feynman(structure)
        
        # 4. Affichage et Sauvegarde
        print("\nCode TikZ généré :\n")
        print(tikz_code)
        
        with open("output.tex", "w") as f:
            # On ajoute un header LaTeX minimal pour que ce soit compilable
            f.write("\\documentclass{standalone}\n")
            f.write("\\usepackage[compat=1.1.0]{tikz-feynman}\n")
            f.write("\\begin{document}\n")
            f.write(tikz_code + "\n")
            f.write("\\end{document}")
            
        print("\n[Succès] Le fichier 'output.tex' a été généré.")
        print("Note : Compilez-le avec LuaLaTeX pour un rendu optimal.")

    except Exception as e:
        print(f"\n[Erreur] Une erreur est survenue lors de la génération : {e}")

if __name__ == "__main__":
    main()