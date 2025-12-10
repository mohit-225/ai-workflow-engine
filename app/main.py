from typing import Dict, Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .graph_engine import (
    EdgeConfig,
    create_graph,
    run_graph,
    get_run_state,
)


from . import summarization_workflow  


app = FastAPI(title="AI Engineering Assignment - Workflow Engine")


class GraphCreateRequest(BaseModel):
    start_node: str
    edges: Dict[str, EdgeConfig]


class GraphCreateResponse(BaseModel):
    graph_id: str


class GraphRunRequest(BaseModel):
    graph_id: str
    initial_state: Dict[str, Any]


@app.post("/graph/create", response_model=GraphCreateResponse)
async def create_graph_endpoint(payload: GraphCreateRequest):
    
    graph_id = create_graph(start_node=payload.start_node, edges=payload.edges)
    return GraphCreateResponse(graph_id=graph_id)


@app.post("/graph/run")
async def run_graph_endpoint(payload: GraphRunRequest):
    
    try:
        result = run_graph(payload.graph_id, payload.initial_state)
        return result
    except KeyError:
        raise HTTPException(status_code=404, detail="Unknown graph_id")


@app.get("/graph/state/{run_id}")
async def get_state_endpoint(run_id: str):

    state = get_run_state(run_id)
    if state is None:
        raise HTTPException(status_code=404, detail="Unknown run_id")
    return {"run_id": run_id, "state": state}
