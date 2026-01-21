import pyfeyngen

reactions = [
    "e+ e- > Z0 > mu+ mu-", # Valide
    "e+ (e- > Z0",          # Erreur : Parenthèse
    "u ubar > X > e+ e-",    # Erreur : Particule X inconnue
    'u ubar > H > (Z0 > e+ e-) (Z0 > mu+ mu-)', # Valide
    'u ubar > H > (Z0 > e+ e-) Z0', # Valide
    'gamma > [ e+ e- ] > gamma', # Valide avec Boucle
    'e- e- > [gamma gamma] > e- e-', # Valide avec Boucle
    'u ubar > H > (Z0 @link > e+ e-) (Z0 @link > mu+ mu-)',
    'u ubar > H > (Z0 @link > e+ e-) (Z0 > mu+ mu- @link)',
    'u ubar @debut > H > (Z0 > e+ e-) (Z0 > mu+ mu-) @debut',
    'u ubar @debut > H > (Z0 > e+ e-) (@debut Z0 > mu+ mu-)',
    'e+ > (e- > @A{blob} > e-) (e- > @A > e-)',
    '(e- > @A > e-) (e- > @A > e-)',
    'e+ e- > [gamma Z0 H] > mu+ mu-',
    'H > (Z0  > @link e+ e-) (Z0  > @link mu+ mu-)',
    'n > @v1{blob} > p e- nubar_e',
    'e- > @box:gamma e- > @box',
    'pibar_e > @v1{blob} > (pi > e+ e-) (pi_e > mu+ mu-)'
]

for r in reactions:
    print(f"Testing: {r}")
    result = pyfeyngen.quick_render(r, debug=True)
    print(result)
    if result.startswith("%"):
        print(f"  ERROR: {result[2:]}")
    else:
        print("  OK: Code généré avec succès.")