import pyfeyngen

reactions = [
    "e+ e- > Z0 > mu+ mu-", # Valide
    "e+ (e- > Z0",          # Erreur : Parenthèse
    "u ubar > X > e+ e-",    # Erreur : Particule X inconnue
    'u ubar > H > (Z0 > e+ e-) (Z0 > mu+ mu-)', 
                 'u ubar > H > (Z0 > e+ e-) Z0',
]

for r in reactions:
    print(f"Testing: {r}")
    result = pyfeyngen.quick_render(r)
    print(result)
    if result.startswith("%"):
        print(f"  ERROR: {result[2:]}")
    else:
        print("  OK: Code généré avec succès.")