import re

def parse_reaction(reaction_str):
    # Nouvelle version : parsing récursif pour cascades complexes
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
                return [recursive_parse(left)] + [recursive_parse(right)]
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
        # Si un token contient un '>' (sous-réaction), on le parse récursivement
        result = []
        for t in tokens:
            if '>' in t:
                result.append(recursive_parse(t))
            else:
                result.append(t)
        return result

    return recursive_parse(reaction_str)