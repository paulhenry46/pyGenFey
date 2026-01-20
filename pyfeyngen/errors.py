class FeyngenError(Exception):
    """Classe de base pour les erreurs pyfeyngen."""
    pass

class InvalidReactionError(FeyngenError):
    """La syntaxe de la chaîne est incorrecte."""
    pass

class UnknownParticleError(FeyngenError):
    """Une particule n'est pas dans physics.py."""
    pass