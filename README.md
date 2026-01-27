<br />
<div align="center">
  <a href="https://github.com/paulhenry46/pyfeyngen">
    <img src="docs/logo.png" alt="Logo" width="80" >
  </a>

  <h3 align="center">Pyfeyngen</h3>

**pyfeyngen** is a high-level Python library designed to transform a natural, string-based particle physics syntax into LaTeX TikZ-Feynman code. It handles complex topologies, including loops, branches, and effective field theory interactions (blobs).

## Installation

```bash
pip install pyfeyngen
```

Note: This library generates TikZ code. To compile the output, you need a LaTeX distribution with the tikz-feynman package installed and use LuaLaTeX.

## 1. Core Syntax Overview

The library parses a reaction string and maps it to a graph structure. The syntax is designed to be readable and mimics the flow of physical processes.

| Component | Syntax | Description |
| --- | --- | --- |
| **Propagation** | `>` | Connects states from left to right. |
| **Simple Particle** | `e-`, `Z0`, `gamma` | Standard particle names (mapped in `physics.py`). |
| **Branching** | `( ... )` | Creates a decay or a split from the current vertex. |
| **Multi-line Loop** | `[p1 p2 ...]` | Creates parallel edges between two vertices. |
| **Anchor** | `@name` | Names a vertex to link it later to another vertex. |
| **Style Attribute** | `{style}` | Applies a style (like `blob`) to a vertex or particle. |

---

## 2. Advanced Features

### Branching & Cascades

To represent a particle decaying into multiple others, use parentheses. You can nest these indefinitely.

* **Example:** `H > (Z0 > e+ e-) (Z0 > mu+ mu-)`
* *Result:* A Higgs boson splitting into two Z bosons, each subsequently decaying into lepton pairs.

### Effective Interactions (Blobs)

To represent a contact interaction or non-resolved vertex, use the `{blob}` attribute on an anchor.

* **Example:** `n > @v1{blob} > p e- nubar_e`
* *Result:* An interaction where the central vertex is rendered as a large shaded disk.

### Anchors & Vertex Linking

Anchors allow you to connect two separate parts of a diagram without a direct flow.

* **Example:** `e+ e- > (mu+ @a > ...) (mu- @a > ...)`
* *Result:* If two vertices share the same `@a` name, the library automatically draws a photon (default) or a specified particle between them.

---

## 3. API Reference

---

### Smart Particle/Label Detection

The library features smart detection of particle names and automatic LaTeX label generation. If a particle name is not found in the default or user dictionary, the system will attempt to intelligently parse the name and deduce its style and LaTeX label.

**How it works:**
- Recognizes common patterns such as Greek letters, charge modifiers (`+`, `-`, `0`), bars (antiparticles), and indices (e.g., `_e`).
- Automatically generates the correct LaTeX label, e.g.:
  - `mu+` → `\mu^{+}`
  - `ubar` → `\bar{u}`
  - `alpha_e` → `\alpha_{e}`
  - `phi-` → `\phi^{-}`
- Deduces the particle style (fermion, boson, scalar, etc.) based on the base name.
- If the name cannot be parsed, a warning is logged and a generic style/label is used.

**Example:**

```python
info = get_info("phi-_")
# info = {"style": "scalar", "label": "\\phi^{-}", "is_anti": False}

info = get_info("ubar")
# info = {"style": "fermion", "label": "\\bar{u}", "is_anti": True}
```

This feature allows you to use a wide range of particle names in your diagrams without needing to predefine every possible variant.

**Function:** `quick_render(reaction_string, debug=False)`

* **Input:** `reaction_string` (str), `debug` (bool, optional)
* **Output:** Generated TikZ string or error message.
* **Description:** Utility function that combines parsing, graph generation, and TikZ export in a single step. If `debug=True`, it displays detailed information about the graph structure and internal steps via the Python logger.

**Enable debug mode:**

To enable debug mode and get detailed information during rendering, use:

```python
from pyfeyngen import quick_render
tikz_code = quick_render("e- > @box:gamma e- > @box", debug=True)
```

This will display debug messages about the graph structure and connections, useful for development or troubleshooting.

**Function:** `parse_reaction(reaction_str)`

* **Input:** `str` (e.g., `"u dbar > W+ > e+ nu_e"`)
* **Output:** A nested list structure representing the hierarchy of the reaction.
* **Logic:** It identifies delimiters `()`, `[]`, and `{}` while respecting operator precedence.

**Class:** `FeynmanGraph(structure)`

* **Purpose:** Converts the parsed structure into a mathematical graph (nodes and edges).
* **Methods:**
* `_process_steps(current_v, steps)`: The recursive engine that traverses the hierarchy to build the topology.
* `_register_anchor(vertex, anchor_dict)`: Maps an anchor name to a specific vertex ID and stores styles.
* `_connect_anchors()`: Post-processing step that creates edges between identical anchor names.

**Function:** `generate_physical_tikz(graph)`

* **Purpose:** Translates the `FeynmanGraph` object into valid LaTeX TikZ code.
* **Key Logic:** * **Single-Declaration Style:** It injects vertex styles (like `[blob]`) only the first time a vertex appears to avoid LaTeX compilation errors.
* **Multi-Bending:** Automatically calculates `bend left` or `bend right` angles if multiple particles exist between the same two nodes.

**Function:** `get_info(particle_name)`


* **Purpose:** A dictionary-based lookup that returns the TikZ style (`fermion`, `boson`, `scalar`, `ghost`) and the LaTeX label for a given string.

**User Dictionary Feature**

You can provide a custom user dictionary to override or extend the default particle definitions. This allows you to specify your own styles, labels, or properties for any particle name.

**Function signature:**

```python
get_info(name, user_dict=None)
```

**Example:**

```python
custom_dict = {
  "X": {"style": "boson", "label": "X^*", "is_anti": False},
  "Y": {"style": "fermion", "label": "Y^-", "is_anti": True}
}
info = get_info("X", user_dict=custom_dict)
# info = {"style": "boson", "label": "X^*", "is_anti": False}
```

This feature is useful for supporting custom particles or overriding the appearance of standard ones in your diagrams.

---

## 4. Full Example Usage

```python
from pyfeyngen import parse_reaction, FeynmanGraph, generate_physical_tikz

# 1. Define the reaction (Higgs to 4 leptons with a contact interaction)
reaction = "H > @v1{blob} > (Z0 > e+ e-) (Z0 > mu+ mu-)"

# 2. Process
structure = parse_reaction(reaction)
graph = FeynmanGraph(structure)
tikz_code = generate_physical_tikz(graph)

# 3. Output
print(tikz_code)

```

**Generated TikZ Output:**

```latex
\feynmandiagram [ horizontal=inx1 to vx1] {
  inx1 -- [scalar, edge label=\(H^{0}\)] vx1[blob],
  vx1 -- [boson, edge label=\(Z^{0}\)] vx2,
  fx1 -- [fermion, edge label=\(e^{+}\)] vx2,
  vx2 -- [fermion, edge label'=\(e^{-}\)] fx2,
  vx1 -- [boson, edge label'=\(Z^{0}\)] vx3,
  fx3 -- [fermion, edge label=\(\mu^{+}\)] vx3,
  vx3 -- [fermion, edge label'=\(\mu^{-}\)] fx4
};

```

---