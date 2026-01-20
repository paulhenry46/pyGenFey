import re

def parse_reaction(reaction_str):
    """
    Transforme une chaîne de réaction en structure de listes imbriquées.
    Exemple: "H > (Z0 > e+ e-) Z0" -> [['H'], [[['Z0'], ['e+', 'e-']], 'Z0']]
    """
    # Nettoyage initial
    s = reaction_str.strip()
    
    # Étape 1 : Séparer par les '>' de premier niveau uniquement
    # On ne split pas si on est à l'intérieur d'une parenthèse
    steps = []
    current_step = ""
    depth = 0
    for char in s:
        if char == '(': depth += 1
        elif char == ')': depth -= 1
        
        if char == '>' and depth == 0:
            steps.append(current_step.strip())
            current_step = ""
        else:
            current_step += char
    steps.append(current_step.strip())
    
    # Étape 2 : Analyser chaque étape pour extraire les particules ou les groupes
    final_structure = []
    for step in steps:
        final_structure.append(_parse_step(step))
        
    return final_structure

def _parse_step(step_str):
    """Analyse une étape pour séparer les particules simples des blocs ( ... )"""
    tokens = []
    i = 0
    while i < len(step_str):
        # Sauter les espaces
        if step_str[i].isspace():
            i += 1
            continue
            
        # Si on trouve une parenthèse, on extrait tout le bloc équilibré
        if step_str[i] == '(':
            start = i + 1
            depth = 1
            i += 1
            while i < len(step_str) and depth > 0:
                if step_str[i] == '(': depth += 1
                elif step_str[i] == ')': depth -= 1
                i += 1
            # On parse récursivement le contenu de la parenthèse
            tokens.append(parse_reaction(step_str[start:i-1]))
        else:
            # Sinon, on lit le nom de la particule jusqu'au prochain espace ou parenthèse
            start = i
            while i < len(step_str) and not step_str[i].isspace() and step_str[i] != '(':
                i += 1
            token = step_str[start:i]
            if token:
                tokens.append(token)
    return tokens

# --- TEST ---
if __name__ == "__main__":
    test1 = "e+ e- > Z0 > mu+ mu-"
    test2 = "H > (Z0 > e+ e-) Z0"
    test3 = "u ubar > H > (Z0 > e+ e-) (Z0 > mu+ mu-)"
    
    for t in [test1, test2, test3]:
        print(f"Input: {t}")
        print(f"Output: {parse_reaction(t)}\n")