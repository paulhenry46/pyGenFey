
class LayeredLayout:
    """
    Computes a layered (column-based) layout for a Feynman graph, assigning x/y positions
    to nodes for visualization. Supports exporting geometry for Inkscape or other tools.
    """
    def __init__(self, graph, x_spacing=150, y_spacing=100):
        """
        Initialize the layout engine with a graph and spacing parameters.
        Args:
            graph: The FeynmanGraph object to layout.
            x_spacing (int): Horizontal distance between columns.
            y_spacing (int): Vertical distance between nodes in a column.
        """
        self.graph = graph
        self.x_spacing = x_spacing
        self.y_spacing = y_spacing
        self.positions = {}

    def _assign_columns(self):
        """
        Assign each node to a column (layer) based on its distance from sources.
        Returns:
            dict: Mapping from node_id to column index.
        """
        columns = {}
        # Identify all nodes present in edges and add to the set
        all_nodes = set(self.graph.nodes)
        all_targets = set()
        for e in self.graph.edges:
            all_nodes.add(e[0])
            all_nodes.add(e[1])
            all_targets.add(e[1])

        # Sources are nodes that are never targets (i.e., have no incoming edges)
        sources = [n for n in all_nodes if n not in all_targets]

        # If no sources (circular graph), pick the first node
        if not sources and all_nodes:
            sources = [list(all_nodes)[0]]

        # Breadth-first assignment of columns
        queue = [(n, 0) for n in sources]
        while queue:
            node_id, col = queue.pop(0)
            columns[node_id] = max(columns.get(node_id, 0), col)

            # Children: nodes that are targets of outgoing edges
            children = [e[1] for e in self.graph.edges if e[0] == node_id]
            for child in children:
                # Avoid infinite loops by only updating if new column is greater
                if columns.get(child, -1) < col + 1:
                    queue.append((child, col + 1))

        # Assign column 0 to any remaining unassigned nodes (safety)
        for node_id in all_nodes:
            if node_id not in columns:
                columns[node_id] = 0
        return columns

    def compute_layout(self):
        """
        Compute the (x, y) positions for each node in the graph based on their assigned columns.
        Returns:
            dict: Mapping from node_id to (x, y) position.
        """
        columns_map = self._assign_columns()
        layers = {}
        for node_id, col in columns_map.items():
            layers.setdefault(col, []).append(node_id)

        if not layers:
            return {}

        # Calculate total height for centering columns
        max_nodes = max(len(nodes) for nodes in layers.values())
        total_height = max_nodes * self.y_spacing

        for col, nodes in layers.items():
            x = col * self.x_spacing
            col_height = len(nodes) * self.y_spacing
            start_y = (total_height - col_height) / 2

            for i, node_id in enumerate(nodes):
                y = start_y + (i * self.y_spacing)
                self.positions[node_id] = (x, y)

        return self.positions

    def get_inkscape_data(self):
        """
        Generate node and edge geometry for Inkscape or other visualization tools.
        Returns:
            dict: Contains 'nodes' (positions and styles) and 'edges' (geometry and labels).
        """
        if not self.positions:
            self.compute_layout()

        # 1. Build node data with positions and styles
        node_data = {}
        for node_id, pos in self.positions.items():
            v_style = getattr(self.graph, 'vertex_styles', {}).get(node_id, "default")
            node_data[node_id] = {
                "x": pos[0],
                "y": pos[1],
                "style": v_style
            }

        # 2. Count edges between each pair for curve distribution
        edge_counts = {}
        for e in self.graph.edges:
            pair = tuple(sorted((e[0], e[1])))
            edge_counts[pair] = edge_counts.get(pair, 0) + 1

        processed_pairs = {}
        geometry_edges = []
        from .physics import get_info

        for src, dst, particle_name in self.graph.edges:
            pair = tuple(sorted((src, dst)))
            # Track the index of the current edge for this pair (1, 2, 3...)
            current_idx = processed_pairs.get(pair, 0) + 1
            processed_pairs[pair] = current_idx

            info = get_info(particle_name)
            total_edges = edge_counts[pair]

            is_curved = total_edges > 1
            bend_value = 0.0

            if is_curved:
                # Spread curves evenly around the straight line
                step = 0.4
                # Center values around 0
                # For 3 edges: 1 -> -0.4, 2 -> 0, 3 -> 0.4
                bend_value = (current_idx - (total_edges + 1) / 2) * step

            geometry_edges.append({
                "start_node": src,
                "end_node": dst,
                "start": self.positions[src],
                "end": self.positions[dst],
                "type": info.get('style', 'fermion'),
                "label": info.get('label', particle_name),
                "is_anti": info.get('is_anti', False),
                "is_curved": is_curved,
                "bend": round(bend_value, 2)
            })

        return {"nodes": node_data, "edges": geometry_edges}