from typing import Tuple, Union, Iterable, Dict, Set

Node = Union[str, int]
Edge = Tuple[Node, Node]


class Graph(object):
    """Graph data structure, undirected by default."""

    def __init__(self, edges: Iterable[Edge] = [], directed: bool = False):
        self._directed = directed
        self._adj: Dict[Node, Dict[Node, int]] = {}  # 邻接表 {节点: {邻居: 边数}}
        self._nodes: Set[Node] = set()

        for edge in edges:
            self.add_edge(edge)

    def has_node(self, node: Node) -> bool:
        """Whether a node is in graph"""
        return node in self._nodes

    def has_edge(self, edge: Edge) -> bool:
        """Whether an edge is in graph"""
        u, v = edge
        if not (self.has_node(u) and self.has_node(v)):
            return False
        return v in self._adj.get(u, {})

    def add_node(self, node: Node):
        """Add a node"""
        if node not in self._nodes:
            self._nodes.add(node)
            self._adj[node] = {}

    def add_edge(self, edge: Edge):
        """Add an edge (u, v). For directed graph, u -> v"""
        u, v = edge
        self.add_node(u)
        self.add_node(v)

        # 更新u的出边
        self._adj[u][v] = self._adj[u].get(v, 0) + 1

        # 如果是无向图，同时更新v的出边
        if not self._directed:
            self._adj[v][u] = self._adj[v].get(u, 0) + 1

    def remove_node(self, node: Node):
        """Remove all references to node"""
        if not self.has_node(node):  # 新增检查
            raise ValueError(f"Node {node} not in graph")

        # 删除所有指向该节点的边
        for u in self._adj:
            if node in self._adj[u]:
                del self._adj[u][node]

        # 删除该节点的邻接信息
        del self._adj[node]
        self._nodes.remove(node)

    def remove_edge(self, edge: Edge):
        """Remove an edge from graph"""
        u, v = edge
        if not self.has_edge(edge):  # 新增检查
            raise ValueError(f"Edge {edge} not in graph")

        # 减少u的出边计数
        if self._adj[u][v] > 1:
            self._adj[u][v] -= 1
        else:
            del self._adj[u][v]

        # 如果是无向图，同时处理v的出边
        if not self._directed:
            if self._adj[v][u] > 1:
                self._adj[v][u] -= 1
            else:
                del self._adj[v][u]

    def indegree(self, node: Node) -> int:
        """Compute indegree for a node"""
        if not self.has_node(node):  # 新增检查
            raise ValueError(f"Node {node} not in graph")
        count = 0
        for u in self._adj:
            if node in self._adj[u]:
                count += self._adj[u][node]
        return count

    def outdegree(self, node: Node) -> int:
        """Compute outdegree for a node"""
        if not self.has_node(node):  # 新增检查
            raise ValueError(f"Node {node} not in graph")
        return sum(self._adj.get(node, {}).values())

    def __str__(self) -> str:
        edges = []
        for u in self._adj:
            for v, count in self._adj[u].items():
                for _ in range(count):
                    edges.append(f"{u} -> {v}" if self._directed else f"{u} -- {v}")
        return f"Graph(nodes={len(self._nodes)}, edges={len(edges)})"

    def __repr__(self) -> str:
        direction = "directed" if self._directed else "undirected"
        return f"<{direction} Graph with {len(self._nodes)} nodes, {len(list(self.edges))} edges>"

    @property
    def edges(self) -> Iterable[Edge]:
        """Helper method to get all edges"""
        edges = set()
        for u in self._adj:
            for v in self._adj[u]:
                if self._directed or (v, u) not in edges:
                    edges.add((u, v))
        return edges
