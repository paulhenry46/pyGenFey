from .errors import UnknownParticleError  # Custom error for unknown particles
from .logger import logger  # Logger for debug and warning messages
import re  # Regular expressions for parsing particle names


# Dictionary of known particles with their style, LaTeX label, and anti-particle status
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
    'H':     {'style': 'scalar', 'label': 'H^{0}', 'is_anti': False}, # Style scalar = dashed or solid line
}


# List of supported Greek letters for LaTeX-style labels
GREEK_LETTERS = [
    'alpha', 'beta', 'gamma', 'delta', 'epsilon', 'zeta', 'eta',
    'theta', 'iota', 'kappa', 'lambda', 'mu', 'nu', 'xi', 'pi',
    'rho', 'sigma', 'tau', 'phi', 'chi', 'psi', 'omega'
]


def get_info(name, user_dict=None):
    """
    Retrieve particle information for a given name, using user_dict or default PARTICLES.
    If the particle is not found, attempts to parse the name and generate a LaTeX label.
    Args:
        name (str): The name of the particle.
        user_dict (dict, optional): User-supplied dictionary of particles.
    Returns:
        dict: Dictionary with keys 'style', 'label', and 'is_anti'.
    """
    if user_dict == None:
        user_dict = {}
    # Check user-supplied dictionary first
    if name in user_dict:
        return user_dict[name]
    # Check built-in PARTICLES dictionary
    elif name in PARTICLES:
        return PARTICLES[name]
    else:
        logger.debug(f"Particle '{name}' is not defined in the library.")

        match = re.match(r"^([a-zA-Z]+?)(bar|\+|\-|0)?(_[a-zA-Z0-9]+)?$", name)

        if not match:
            logger.warning(f"Particle '{name}' is unreadable.")
            return {"style": "fermion", "label": name, "is_anti": False}

        base, modifier, index = match.groups()

        # 1. Handle the BASE (e.g., alpha -> \alpha)
        latex_base = rf"\{base}" if base in GREEK_LETTERS else base
        
        # 2. Handle the INDEX (e.g., _e -> _{e})
        index_str = f"_{{{index[1:]}}}" if index else ""

        # 3. FINAL ASSEMBLY (convert 'bar' to LaTeX command)
        is_anti = False
        if modifier == 'bar':
            is_anti = True
            label = rf"\bar{{{latex_base}}}{index_str}"  # e.g., \bar{\alpha}_{e}
        elif modifier in ['+', '-', '0']:
            label = f"{latex_base}^{{{modifier}}}{index_str}" # e.g., \alpha^{+}_{e}
            if modifier == '+' and base in ['e', 'mu', 'tau']:
                is_anti = True
        else:
            label = f"{latex_base}{index_str}"

        # 4. Deduce the style
        style = "fermion"
        if base in ['phi', 'h', 'H', 'S']:
            style = "scalar"
        elif base in ['W', 'Z', 'gamma', 'g']:
            style = "boson"  # Simplified for this example

        return {
            "style": style,
            "label": label,
            "is_anti": is_anti
        }