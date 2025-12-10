
A lightweight workflow/agent execution engine built with Python and FastAPI.
This project was developed as part of an AI Engineering backend assignment to demonstrate a minimal workflow system capable of executing node-based steps, maintaining shared state, and supporting branching and looping logic.

The engine runs entirely in memory and focuses on clarity, structure, and correctness. A simple text-summarization workflow is included to illustrate how the engine behaves in a real flow.

Features:

Define workflows using plain Python functions (nodes)

Shared state passed from step to step

JSON-defined edges to control execution order

Conditional branching (if/else)

Looping logic (repeat until condition is met)

FastAPI endpoints to create and run workflows

Execution logs for debugging

In-memory graph and run storage

Project Structure:

app/

├── main.py                     # FastAPI routes and request handling

├── graph_engine.py             # Core workflow engine (nodes, edges, execution)

├── workflows.py                # Example summarization workflow

├── tools.py                    # Optional tool registry

└── __init__.py

Example Workflow: Text Summarization

The example workflow demonstrates how nodes and conditions come together:

Split text into chunks

Generate a summary for each chunk

Merge summaries into one block

Refine the final summary

Loop until the summary length meets a given limit

Everything is rule-based — no ML models required.

API Endpoints:
POST /graph/create

Create a workflow by providing a JSON description of nodes and edges.
Returns a graph_id.

POST /graph/run

Run an existing workflow using an initial state.
Returns the run_id, final state, and execution log.

GET /graph/state/{run_id}

Retrieve the stored state of a completed workflow run.

Swagger UI is available at:

http://127.0.0.1:8000/docs

How to Run the Project:
1. Setup environment
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt

2. Start the server
uvicorn app.main:app --reload

3. Open the API docs
http://127.0.0.1:8000/docs


Use the interactive docs to create workflows, run them, and inspect results.

How It Works (Short Overview):

Each node is a simple Python function that reads and modifies a shared state dict

Edges decide the next node or evaluate conditions

The engine walks through nodes until no more transitions are available

Looping is achieved through conditional edges

Graphs and runs are stored in memory for simplicity

The design keeps things small and approachable while still showing essential backend concepts.

Possible Improvements:

If extended further, the project could include:

Database storage for graphs and runs

WebSocket streaming for real-time logs

Async support for long-running nodes

UI for visualizing workflow graphs

Better error handling and validation

Why This Approach:

The objective was to build a clean and understandable workflow engine.
The emphasis stayed on:

clear logic

easy-to-read code

simple but effective workflow execution

separation of concerns (engine, workflow, API)

This keeps the system small but realistic.
