import re

def parse_reaction(reaction_str):
    # Parsing récursif robuste pour cascades et branches multiples
    def recursive_parse(s):
        s = s.strip()
        # Si la chaîne commence par une parenthèse, on extrait le bloc
        if s.startswith("(") and s.endswith(")"):
            s = s[1:-1]
        # Sépare au niveau du premier '>' non inclus dans parenthèses
        depth = 0
        for i, c in enumerate(s):
            if c == '(': depth += 1
            elif c == ')': depth -= 1
            elif c == '>' and depth == 0:
                left = s[:i].strip()
                right = s[i+1:].strip()
                # On parse la partie gauche (entrée ou parent)
                left_parsed = recursive_parse(left)
                # On parse la partie droite (peut contenir plusieurs branches)
                # On découpe la droite en tokens principaux (hors parenthèses)
                tokens = []
                buf = ''
                d = 0
                for ch in right:
                    if ch == '(':
                        d += 1
                    elif ch == ')':
                        d -= 1
                    if ch == ' ' and d == 0:
                        if buf.strip():
                            tokens.append(buf.strip())
                        buf = ''
                    else:
                        buf += ch
                if buf.strip():
                    tokens.append(buf.strip())
                # On parse chaque branche, on ignore les branches vides
                right_parsed = [recursive_parse(tok) for tok in tokens if tok]
                # Si une seule branche, on évite la liste inutile
                if len(right_parsed) == 1:
                    right_parsed = right_parsed[0]
                return [left_parsed, right_parsed]
        # Si pas de '>' au niveau racine, on split par espaces hors parenthèses
        tokens = []
        buf = ''
        depth = 0
        for c in s:
            if c == '(': depth += 1
            elif c == ')': depth -= 1
            if c == ' ' and depth == 0:
                if buf:
                    tokens.append(buf)
                    buf = ''
            else:
                buf += c
        if buf:
            tokens.append(buf)
        return tokens

    def clean_empty_branches(tree):
        if isinstance(tree, list):
            # On filtre les sous-listes vides ou contenant uniquement des sous-listes vides
            cleaned = [clean_empty_branches(x) for x in tree if x != []]
            # On retire les branches qui sont devenues vides
            return [x for x in cleaned if x != []]
        return tree

    return clean_empty_branches(recursive_parse(reaction_str))