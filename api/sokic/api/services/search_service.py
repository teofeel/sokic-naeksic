import re
from datetime import datetime
from typing import List, Tuple, Any

from sokic.api.models.graph import Graph
from sokic.api.models.node import Node
from sokic.api.models.edge import Edge


class FilterParseError(ValueError):
    """Raised when a filter query string cannot be parsed."""
    pass


class FilterTypeError(TypeError):
    """Raised when the filter value cannot be coerced to the attribute's type."""
    pass


COMPARATORS = [">=", "<=", "!=", "==", ">", "<"]


def _parse_filter_query(query: str) -> Tuple[str, str, str]:
    """
    Parse:  <attribute_name> <comparator> <value>
    Returns (attr_name, comparator, raw_value_str)
    Raises FilterParseError on bad syntax.
    """
    query = query.strip()
    for comp in COMPARATORS:
        m = re.match(rf"^(.+?)\s*({re.escape(comp)})\s*(.+)$", query)
        if m:
            return m.group(1).strip(), m.group(2), m.group(3).strip()
    raise FilterParseError(
        f"Invalid filter: '{query}'. "
        f"Expected: <attribute> <comparator> <value>  "
        f"(comparators: {COMPARATORS})"
    )


def _coerce_value(raw: str, reference: Any) -> Any:
    """
    Coerce the user-supplied string `raw` to the same Python type as
    `reference` (the actual value stored on the node).
    Raises FilterTypeError if coercion fails.
    """
    if isinstance(reference, bool):
        if raw.lower() in ("true", "1", "yes"):
            return True
        if raw.lower() in ("false", "0", "no"):
            return False
        raise FilterTypeError(f"Cannot convert '{raw}' to bool (use true/false).")

    if isinstance(reference, int):
        try:
            return int(raw)
        except ValueError:
            raise FilterTypeError(f"Cannot convert '{raw}' to int.")

    if isinstance(reference, float):
        try:
            return float(raw)
        except ValueError:
            raise FilterTypeError(f"Cannot convert '{raw}' to float.")

    if isinstance(reference, datetime):
        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d.%m.%Y", "%Y/%m/%d"):
            try:
                return datetime.strptime(raw, fmt)
            except ValueError:
                continue
        raise FilterTypeError(
            f"Cannot parse '{raw}' as date. "
            "Supported: YYYY-MM-DD, DD/MM/YYYY, DD.MM.YYYY"
        )

    return str(raw)


def _apply_comparator(node_val: Any, comparator: str, filter_val: Any) -> bool:
    try:
        ops = {"==": lambda a, b: a == b, "!=": lambda a, b: a != b,
               ">":  lambda a, b: a >  b, ">=": lambda a, b: a >= b,
               "<":  lambda a, b: a <  b, "<=": lambda a, b: a <= b}
        return ops[comparator](node_val, filter_val)
    except TypeError:
        return False


class SearchService:
    """
    Full-text search + structured filter for Graph objects.

    Both operations return a NEW subgraph, enabling chaining:
        G1 --filter--> G2 --search--> G3 --filter--> G4 ...
    """

    # ── SEARCH ────────────────────────────────────────────────────────── #

    def search_nodes(self, graph: Graph, query: str) -> List[Node]:
        q = query.lower()
        result: List[Node] = []

        for node in graph.nodes.values():
            for attr_name, attr_value in node.data.items():
                if q in attr_name.lower() or q in str(attr_value).lower():
                    result.append(node)
                    break

        return result

    def search_subgraph(self, graph: Graph, query: str) -> Graph:
        """Return a subgraph of nodes matching `query` + edges between them."""
        return self._build_subgraph(graph, self.search_nodes(graph, query))

    def search_edges(self, graph: Graph, query: str) -> List[Edge]:
        """
        Edges whose id, source id, target id, or any data value
        contains `query` (case-insensitive).
        """
        q = query.lower()
        result: List[Edge] = []

        for edge in graph.edges.values():
            if q in edge.source.lower() or q in edge.target.lower() or q in edge.id.lower():
                result.append(edge)
                continue
            if hasattr(edge, "data") and edge.data:
                if any(q in str(v).lower() for v in edge.data.values()):
                    result.append(edge)

        return result

    # ── FILTER ────────────────────────────────────────────────────────── #

    def filter_nodes(self, graph: Graph, filter_query: str) -> List[Node]:
        """
        Structured filter:  <attribute> <comparator> <value>
        Examples:
            "born >= 1990"
            "role == Sin"
            "name != Marko"

        Raises FilterParseError for bad syntax, FilterTypeError for type mismatch.
        """
        attr, comparator, raw_value = _parse_filter_query(filter_query)
        result: List[Node] = []

        for node in graph.nodes.values():
            if attr not in node.data:
                continue
            node_val = node.data[attr]
            filter_val = _coerce_value(raw_value, node_val)   # raises FilterTypeError
            if _apply_comparator(node_val, comparator, filter_val):
                result.append(node)

        return result

    def filter_subgraph(self, graph: Graph, filter_query: str) -> Graph:
        """Return a subgraph of nodes matching the filter + edges between them."""
        return self._build_subgraph(graph, self.filter_nodes(graph, filter_query))

    # ── HELPERS ───────────────────────────────────────────────────────── #

    def _build_subgraph(self, graph: Graph, nodes: List[Node]) -> Graph:
        node_ids = {n.id for n in nodes}
        sub = Graph(direction=graph.direction, cycle_policy=graph.cycle_policy)

        for node in nodes:
            sub.nodes[node.id] = node

        for edge in graph.edges.values():
            if edge.source in node_ids and edge.target in node_ids:
                sub.edges[edge.id] = edge

        return sub