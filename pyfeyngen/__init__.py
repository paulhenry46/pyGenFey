# pyfeyngen/__init__.py

from .parser import parse_reaction
from .layout import FeynmanGraph
from .exporter import generate_physical_tikz
from .errors import InvalidReactionError, UnknownParticleError
from .logger import setup_logging, logger

__version__ = "1.0.0"
__author__ = "Saux Paulhenry & Contributors"

def quick_render(reaction_string, debug=False):
    if debug:
        setup_logging(True)
    try:
        structure = parse_reaction(reaction_string)
        graph = FeynmanGraph(structure)
        logger.debug(f"\nNoeuds créés : {graph.v_count} vertex, {graph.in_count} entrées, {graph.f_count} sorties.")
    
        logger.debug("\nListe des connexions (Edges) :")
        logger.debug(f"{'Source':<10} | {'Cible':<10} | {'Particule':<10}")
        logger.debug("-" * 35)
        for src, dst, particle in graph.edges:
            logger.debug(f"{src:<10} | {dst:<10} | {particle:<10}")
        logger.debug("-" * 35)
        logger.debug("\nListe des Ancres :")
        logger.debug(graph.anchor_points)

        return generate_physical_tikz(graph)
    except InvalidReactionError as e:
        return f"% Erreur de syntaxe : {e}"
    except UnknownParticleError as e:
        return f"% Erreur physique : {e}"
    except Exception as e:
        return f"% Erreur inattendue : {e}"

# On définit ce qui est accessible lors d'un "from pyfeyngen import *"
__all__ = ["parse_reaction", "FeynmanGraph", "generate_physical_tikz", "quick_render"]