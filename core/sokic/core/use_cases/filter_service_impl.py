import re
from datetime import datetime
from typing import Any, List, Tuple

from sokic.api.services import FilterService
from sokic.api.models import Graph, Node

from sokic.core.use_cases.graph_utils import build_subgraph


# ── ERRORS ────────────────────────────────────────────────────────────── #

class FilterParseError(ValueError):
    """Raised when a filter query string cannot be parsed."""
    pass


class FilterTypeError(TypeError):
    """Raised when the filter value cannot be coerced to the attribute's type."""
    pass


# ── Const and Helpers ───────────────────────────────────────────────── #

COMPARATORS = [">=", "<=", "!=", "==", ">", "<"]


def _parse_filter_query(query: str) -> Tuple[str, str, str]:
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
        ops = {
            "==": lambda a, b: a == b,
            "!=": lambda a, b: a != b,
            ">":  lambda a, b: a >  b,
            ">=": lambda a, b: a >= b,
            "<":  lambda a, b: a <  b,
            "<=": lambda a, b: a <= b,
        }
        return ops[comparator](node_val, filter_val)
    except TypeError:
        return False


# ── Implementation ────────────────────────────────────────────────────── #

class FilterServiceImpl(FilterService):

    def filter_nodes(self, graph: Graph, filter_query: str) -> List[Node]:
        attr, comparator, raw_value = _parse_filter_query(filter_query)
        result: List[Node] = []
        for node in graph.nodes.values():
            if attr not in node.data:
                continue
            node_val = node.data[attr]
            filter_val = _coerce_value(raw_value, node_val)
            if _apply_comparator(node_val, comparator, filter_val):
                result.append(node)
        return result

    def filter_subgraph(self, graph: Graph, filter_query: str) -> Graph:
        return build_subgraph(graph, self.filter_nodes(graph, filter_query))

