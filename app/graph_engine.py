from typing import Callable, Dict, Any, List, Optional
from pydantic import BaseModel
import uuid

State = Dict[str, Any]
NodeFunc = Callable[[State], State]


class EdgeConfig(BaseModel):
    next: Optional[str] = None

    condition_key: Optional[str] = None       
    condition_op: Optional[str] = None        
    condition_value: Optional[Any] = None     
    if_true: Optional[str] = None             
    if_false: Optional[str] = None            


class Graph(BaseModel):
    id: str
    start_node: str
    edges: Dict[str, EdgeConfig]


class RunLogEntry(BaseModel):
    node: str
    state_snapshot: State


class RunResult(BaseModel):
    run_id: str
    final_state: State
    log: List[RunLogEntry]


TOOL_REGISTRY: Dict[str, Callable[..., Any]] = {}
NODE_REGISTRY: Dict[str, NodeFunc] = {}
GRAPHS: Dict[str, Graph] = {}
RUNS: Dict[str, Dict[str, Any]] = {}


def register_tool(name: str, func: Callable[..., Any]) -> None:
    TOOL_REGISTRY[name] = func


def get_tool(name: str) -> Callable[..., Any]:
    return TOOL_REGISTRY[name]


def register_node(name: str, func: NodeFunc) -> None:
    NODE_REGISTRY[name] = func


def create_graph(start_node: str, edges: Dict[str, EdgeConfig]) -> str:
    graph_id = str(uuid.uuid4())
    graph = Graph(id=graph_id, start_node=start_node, edges=edges)
    GRAPHS[graph_id] = graph
    return graph_id


def _eval_condition(state: State, edge: EdgeConfig) -> bool:
    key = edge.condition_key
    op = edge.condition_op
    target = edge.condition_value

    if key is None or op is None:
        return False

    value = state.get(key)
    if value is None:
        return False

    if op == ">":
        return value > target
    if op == "<":
        return value < target
    if op == ">=":
        return value >= target
    if op == "<=":
        return value <= target
    if op == "==":
        return value == target
    if op == "!=":
        return value != target

    return False


def run_graph(graph_id: str, initial_state: State) -> RunResult:
    graph = GRAPHS[graph_id]

    state: State = dict(initial_state)  
    log: List[RunLogEntry] = []

    current = graph.start_node

    while current is not None:
        node_fn = NODE_REGISTRY[current]
        state = node_fn(state)

        log.append(RunLogEntry(node=current, state_snapshot=dict(state)))

        edge = graph.edges.get(current)
        if edge is None:
            current = None
            break

        if edge.condition_key:
            cond = _eval_condition(state, edge)
            current = edge.if_true if cond else edge.if_false
        else:
            current = edge.next

    run_id = str(uuid.uuid4())
    RUNS[run_id] = {"state": state, "log": log}
    return RunResult(run_id=run_id, final_state=state, log=log)


def get_run_state(run_id: str) -> Optional[State]:
    run = RUNS.get(run_id)
    if not run:
        return None
    return run["state"]
