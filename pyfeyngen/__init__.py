# pyfeyngen/__init__.py

from .parser import parse_reaction
from .layout import FeynmanGraph
from .exporter import generate_physical_tikz
from .errors import InvalidReactionError, UnknownParticleError

__version__ = "1.0.0"
__author__ = "Saux Paulhenry & Contributors"

def quick_render(reaction_string):
    try:
        structure = parse_reaction(reaction_string)
        graph = FeynmanGraph(structure)
        return generate_physical_tikz(graph)
    except InvalidReactionError as e:
        return f"% Erreur de syntaxe : {e}"
    except UnknownParticleError as e:
        return f"% Erreur physique : {e}"
    except Exception as e:
        return f"% Erreur inattendue : {e}"

# On définit ce qui est accessible lors d'un "from pyfeyngen import *"
__all__ = ["parse_reaction", "FeynmanGraph", "generate_physical_tikz", "quick_render"]