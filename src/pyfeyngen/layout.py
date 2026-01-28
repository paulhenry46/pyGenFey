
# Import the logger for debug or information messages
from .logger import logger


class FeynmanGraph:
    """
    Represents a Feynman diagram as a graph structure with nodes (vertices), edges (connections),
    and support for anchors and vertex styles. Builds the graph from a parsed reaction structure.
    """
    def __init__(self, structure):
        # Lists for graph nodes and edges
        self.nodes = []      
        self.edges = []      
        # Counters for unique vertex, input, and final node names
        self.v_count = 0
        self.in_count = 0
        self.f_count = 0
        # Anchor points for named vertices (e.g., for connecting special points)
        self.anchor_points = {} 
        # Stores vertex styles (e.g., { "vx1": "blob" })
        self.vertex_styles = {}
        # Build the graph from the provided structure
        self.build_graph(structure)


    def new_v(self):
        """Create a new unique vertex name."""
        self.v_count += 1
        return f"vx{self.v_count}"


    def new_in(self):
        """Create a new unique input node name."""
        self.in_count += 1
        return f"inx{self.in_count}"


    def new_f(self):
        """Create a new unique final/output node name."""
        self.f_count += 1
        return f"fx{self.f_count}"


    def build_graph(self, structure):
        """
        Build the Feynman graph from the parsed structure.
        Handles input particles, anchors, cascades, and connects anchors at the end.
        Args:
            structure (list): Parsed reaction structure from the parser.
        """
        first_step = structure[0]

        # Extract input particles, anchors, and cascades from the first step
        in_particles = [p for p in first_step if isinstance(p, (str, dict)) and 'anchor' not in str(p) and 'loop' not in str(p) and 'cascade' not in str(p)]
        in_anchors = [p for p in first_step if isinstance(p, dict) and 'anchor' in p]
        in_cascades = [p for p in first_step if isinstance(p, (list, dict)) and ('cascade' in str(p) or isinstance(p, list))]

        if in_particles:
            # Create a starting vertex for input particles
            v_start = self.new_v()
            for a in in_anchors:
                self._register_anchor(v_start, a)
            for p in in_particles:
                p_name = p['name'] if isinstance(p, dict) else p
                in_node = self.new_in()
                self.edges.append((in_node, v_start, p_name))
            self._process_steps(v_start, structure[1:])

        elif in_cascades:
            # Handle cascades (nested reactions)
            for item in in_cascades:
                cascade = item['cascade'] if isinstance(item, dict) else item
                v_root = self.new_v()

                # If the root has a blob style, record it
                if isinstance(item, dict) and item.get('style') == 'blob':
                    self.vertex_styles[v_root] = 'blob'

                p_start = cascade[0][0]
                p_name = p_start['name'] if isinstance(p_start, dict) else p_start

                in_node = self.new_in()
                self.edges.append((in_node, v_root, p_name))

                # Register anchors in the cascade
                for t in cascade[0]:
                    if isinstance(t, dict) and 'anchor' in t:
                        self._register_anchor(v_root, t)
                self._process_steps(v_root, cascade[1:])

        # Connect all anchors at the end
        self._connect_anchors()


    def _process_steps(self, current_v, steps):
        """
        Recursively process each step in the reaction structure, building edges and handling
        anchors, loops, cascades, and final particles.
        Args:
            current_v (str): The current vertex being processed.
            steps (list): Remaining steps to process.
        """
        if not steps:
            return
        step = steps[0]

        # Extract anchors, loops, and particles from the step
        anchors = [item for item in step if isinstance(item, dict) and 'anchor' in item]
        loops = [item for item in step if isinstance(item, dict) and 'loop' in item]
        # Capture anything that can be a particle (str, style dict, or cascade)
        particles = [item for item in step if isinstance(item, (str, list)) or (isinstance(item, dict) and 'anchor' not in item and 'loop' not in item)]

        # Register anchors and detect blob style
        for a in anchors:
            self._register_anchor(current_v, a)

        for item in step:
            if isinstance(item, dict) and item.get('style') == 'blob':
                self.vertex_styles[current_v] = 'blob'

        # Handle loops (multi-particle bends)
        if loops:
            loop_data = loops[0]
            v_loop_end = self.new_v()
            if loop_data.get('style') == 'blob':
                self.vertex_styles[v_loop_end] = 'blob'
            for p in loop_data['loop']:
                self.edges.append((current_v, v_loop_end, p))
            self._process_steps(v_loop_end, steps[1:])
            return

        if not particles:
            self._process_steps(current_v, steps[1:])
            return

        # Handle particles (outputs or propagation)
        # If this is the last step or there are multiple particles, treat as outputs/branches
        if len(steps) == 1 or len(particles) > 1:
            for item in particles:
                if isinstance(item, (list, dict)) and ('cascade' in str(item) or isinstance(item, list)):
                    # This is a cascade (nested reaction)
                    cascade = item['cascade'] if isinstance(item, dict) else item
                    v_branch = self.new_v()
                    if isinstance(item, dict) and item.get('style') == 'blob':
                        self.vertex_styles[v_branch] = 'blob'

                    # Take the bridge particle
                    p_start = cascade[0][0]
                    p_name = p_start['name'] if isinstance(p_start, dict) else p_start
                    self.edges.append((current_v, v_branch, p_name))
                    self._process_steps(v_branch, cascade[1:])
                else:
                    # This is a final particle (output)
                    p_name = item['name'] if isinstance(item, dict) else item
                    f_node = self.new_f()
                    self.edges.append((current_v, f_node, p_name))

        # If there is only one particle and more steps, propagate to next vertex
        else:
            item = particles[0]
            p_name = item['name'] if isinstance(item, dict) else item
            v_next = self.new_v()
            self.edges.append((current_v, v_next, p_name))
            self._process_steps(v_next, steps[1:])


    def _register_anchor(self, vertex, anchor_dict):
        """
        Register an anchor point for a vertex, optionally marking it with a style.
        Args:
            vertex (str): The vertex name.
            anchor_dict (dict): Anchor information (may include style and particle).
        """
        name = anchor_dict['anchor']
        if anchor_dict.get('style') == 'blob':
            self.vertex_styles[vertex] = 'blob'

        if name not in self.anchor_points:
            self.anchor_points[name] = []
        self.anchor_points[name].append({
            'vertex': vertex,
            'particle': anchor_dict.get('particle')
        })


    def _connect_anchors(self):
        """
        Connect all registered anchors by creating edges between consecutive anchor points
        with the specified particle (or 'gamma' by default).
        """
        for name, points in self.anchor_points.items():
            if len(points) >= 2:
                for i in range(len(points) - 1):
                    src = points[i]['vertex']
                    dst = points[i+1]['vertex']
                    p_name = points[i]['particle'] or "gamma"
                    self.edges.append((src, dst, p_name))
