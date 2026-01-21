
# pyfeyngen/__init__.py
# Main initialization file for the pyfeyngen package.

from .parser import parse_reaction
from .layout import FeynmanGraph
from .exporter import generate_physical_tikz
from .errors import InvalidReactionError, UnknownParticleError
from .logger import setup_logging, logger

__version__ = "1.0.0"
__author__ = "Saux Paulhenry & Contributors"

def quick_render(reaction_string, user_dict=None, debug=False):

    # Enable debug logging if requested
    if debug:
        setup_logging(True)
    try:
        # Parse the reaction string into a structured format
        structure = parse_reaction(reaction_string)
        # Build the Feynman graph from the parsed structure
        graph = FeynmanGraph(structure)
        # Log graph node and edge information for debugging
        logger.debug(f"\nNodes created: {graph.v_count} vertex, {graph.in_count} inputs, {graph.f_count} outputs.")
        logger.debug("\nEdge list:")
        logger.debug(f"{'Source':<10} | {'Target':<10} | {'Particle':<10}")
        logger.debug("-" * 35)
        for src, dst, particle in graph.edges:
            logger.debug(f"{src:<10} | {dst:<10} | {particle:<10}")
        logger.debug("-" * 35)
        logger.debug("\nAnchor points:")
        logger.debug(graph.anchor_points)

        # Generate the TikZ code from the graph and user dictionary
        return generate_physical_tikz(graph, user_dict)
    except InvalidReactionError as e:
        # Return a LaTeX comment for syntax errors
        return f"% Syntax error: {e}"
    except UnknownParticleError as e:
        # Return a LaTeX comment for unknown particle errors
        return f"% Physics error: {e}"
    except Exception as e:
        # Return a LaTeX comment for any unexpected error
        return f"% Unexpected error: {e}"

# Define what is accessible with 'from pyfeyngen import *'
__all__ = ["parse_reaction", "FeynmanGraph", "generate_physical_tikz", "quick_render"]