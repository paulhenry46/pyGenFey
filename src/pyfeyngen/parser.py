from .errors import InvalidReactionError

def parse_reaction(reaction_str):
    """
    Parse a reaction string into a nested list structure.
    Supports branching (...), multi-particle loops [...], anchors @, and style attributes {...}.
    Args:
        reaction_str (str): The reaction string to parse.
    Returns:
        list: Nested list structure representing the parsed reaction.
    Raises:
        InvalidReactionError: If the input string is empty or delimiters are unbalanced.
    """
    if not reaction_str.strip():
        raise InvalidReactionError("Reaction string is empty.")
    # Check for balanced delimiters
    if reaction_str.count('(') != reaction_str.count(')'):
        raise InvalidReactionError("Unbalanced parentheses.")
    if reaction_str.count('[') != reaction_str.count(']'):
        raise InvalidReactionError("Unbalanced brackets.")
    if reaction_str.count('{') != reaction_str.count('}'):
        raise InvalidReactionError("Unbalanced braces.")

    s = reaction_str.strip()
    steps = []
    current_step = ""
    depth = 0

    # Split the reaction string by top-level '>' (not inside parentheses)
    for char in s:
        if char == '(': depth += 1
        elif char == ')': depth -= 1

        if char == '>' and depth == 0:
            steps.append(current_step.strip())
            current_step = ""
        else:
            current_step += char
    steps.append(current_step.strip())

    final_structure = []
    for step in steps:
        if step:
            final_structure.append(_parse_step(step))
        
    return final_structure

def _parse_step(step_str):
    """
    Analyze a step to separate particles, cascades (parentheses), loops (brackets), anchors (@), and styles (braces).
    Args:
        step_str (str): The step string to analyze.
    Returns:
        list: List of tokens representing the parsed step.
    """
    tokens = []
    i = 0
    while i < len(step_str):
        # Skip whitespace
        if step_str[i].isspace():
            i += 1
            continue

        # 1. Handle parentheses for cascades (nested reactions)
        if step_str[i] == '(':  # Start of a cascade
            start = i + 1
            depth = 1
            i += 1
            while i < len(step_str) and depth > 0:
                if step_str[i] == '(': depth += 1
                elif step_str[i] == ')': depth -= 1
                i += 1
            # Recursively parse the content inside parentheses
            tokens.append(parse_reaction(step_str[start:i-1]))

        # 2. Handle brackets for loops (multi-particle bends)
        elif step_str[i] == '[':
            start = i + 1
            depth = 1
            i += 1
            while i < len(step_str) and depth > 0:
                if step_str[i] == '[': depth += 1
                elif step_str[i] == ']': depth -= 1
                i += 1
            # Split loop content into individual particles
            loop_content = [p.strip() for p in step_str[start:i-1].split() if p.strip()]
            tokens.append({'loop': loop_content})

        # 3. Handle anchors (e.g., @vertex or @vertex:particle)
        elif step_str[i] == '@':
            start = i + 1
            # Stop at whitespace or any opening delimiter
            while i < len(step_str) and not step_str[i].isspace() and step_str[i] not in '([{':
                i += 1
            anchor_text = step_str[start:i]
            if ':' in anchor_text:
                name, part = anchor_text.split(':', 1)
                tokens.append({'anchor': name, 'particle': part})
            else:
                tokens.append({'anchor': anchor_text, 'particle': None})

        # 4. Handle style attributes in braces (e.g., {blob})
        elif step_str[i] == '{':
            start = i + 1
            depth = 1
            i += 1
            while i < len(step_str) and depth > 0:
                if step_str[i] == '{': depth += 1
                elif step_str[i] == '}': depth -= 1
                i += 1
            attr_content = step_str[start:i-1].strip()

            # Apply the attribute to the last added element
            if tokens:
                last_item = tokens[-1]
                if isinstance(last_item, dict):
                    last_item['style'] = attr_content
                elif isinstance(last_item, str):
                    tokens[-1] = {'name': last_item, 'style': attr_content}
                elif isinstance(last_item, list):
                    tokens[-1] = {'cascade': last_item, 'style': attr_content}
            continue  # Do not increment i twice

        # 5. Handle particle names (default case)
        else:
            start = i
            # Stop at whitespace or any opening delimiter
            while i < len(step_str) and not step_str[i].isspace() and step_str[i] not in '([@{':
                i += 1
            token = step_str[start:i]
            if token:
                tokens.append(token)

    return tokens