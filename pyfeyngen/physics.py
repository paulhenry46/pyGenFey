# physics.py
from .errors import UnknownParticleError
# physics.py

PARTICLES = {
    # Quarks
    'u':     {'style': 'fermion', 'label': 'u', 'is_anti': False},
    'ubar':  {'style': 'fermion', 'label': '\\bar{u}', 'is_anti': True},
    'd':     {'style': 'fermion', 'label': 'd', 'is_anti': False},
    'dbar':  {'style': 'fermion', 'label': '\\bar{d}', 'is_anti': True},
    't':     {'style': 'fermion', 'label': 't', 'is_anti': False},
    'tbar':  {'style': 'fermion', 'label': '\\bar{t}', 'is_anti': True},
    
    # Leptons
    'e-':    {'style': 'fermion', 'label': 'e^{-}', 'is_anti': False},
    'e+':    {'style': 'fermion', 'label': 'e^{+}', 'is_anti': True},
    'mu-':   {'style': 'fermion', 'label': '\\mu^{-}', 'is_anti': False},
    'mu+':   {'style': 'fermion', 'label': '\\mu^{+}', 'is_anti': True},
    'tau-':  {'style': 'fermion', 'label': '\\tau^{-}', 'is_anti': False},
    'tau+':  {'style': 'fermion', 'label': '\\tau^{+}', 'is_anti': True},
    'nu_e':  {'style': 'fermion', 'label': '\\nu_{e}', 'is_anti': False},
    
    # Bosons
    'Z0':    {'style': 'boson', 'label': 'Z^{0}', 'is_anti': False},
    'W+':    {'style': 'charged boson', 'label': 'W^{+}', 'is_anti': False},
    'W-':    {'style': 'charged boson', 'label': 'W^{-}', 'is_anti': True},
    'gamma': {'style': 'photon', 'label': '\\gamma', 'is_anti': False},
    'g':     {'style': 'gluon', 'label': 'g', 'is_anti': False},
    'H':     {'style': 'scalar', 'label': 'H^{0}', 'is_anti': False}, # Style scalar = ligne tiretée ou pleine
}

def get_info(name):
    # Retourne les infos ou un style par défaut si inconnu
    if name not in PARTICLES:
        raise UnknownParticleError(f"La particule '{name}' n'est pas définie dans la bibliothèque.")
    return PARTICLES[name]