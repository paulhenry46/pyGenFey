# physics.py
from .errors import UnknownParticleError
PARTICLES = {
    'e-':    {'style': 'fermion', 'label': 'e^{-}', 'is_anti': False},
    'e+':    {'style': 'fermion', 'label': 'e^{+}', 'is_anti': True},
    'mu-':   {'style': 'fermion', 'label': '\\mu^{-}', 'is_anti': False},
    'mu+':   {'style': 'fermion', 'label': '\\mu^{+}', 'is_anti': True},
    'u':     {'style': 'fermion', 'label': 'u',         'is_anti': False},
    'ubar':  {'style': 'fermion', 'label': '\\bar{u}',  'is_anti': True},
    'Z0':    {'style': 'boson',   'label': 'Z^{0}',    'is_anti': False},
    'gamma': {'style': 'photon',  'label': '\\gamma',   'is_anti': False},
    'H':     {'style': 'plain',   'label': 'H^{0}',     'is_anti': False},
}

def get_info(name):
    # Retourne les infos ou un style par défaut si inconnu
    if name not in PARTICLES:
        raise UnknownParticleError(f"La particule '{name}' n'est pas définie dans la bibliothèque.")
    return PARTICLES[name]