from typing import List

from .graph_engine import register_node, register_tool, State


# Example tool (just to show a tool registry in use)
def simple_length_tool(text: str) -> int:
    return len(text)


register_tool("length", simple_length_tool)


def split_text_node(state: State) -> State:
    """
    Node 1: Split text into chunks of roughly max_chunk_size characters,
    without splitting in the middle of words.
    """
    text = state.get("text", "")
    max_chunk_size = state.get("max_chunk_size", 200)

    words = text.split()
    chunks: List[str] = []
    current: List[str] = []

    for w in words:
        candidate = " ".join(current + [w])
        if len(candidate) <= max_chunk_size:
            current.append(w)
        else:
            if current:
                chunks.append(" ".join(current))
            current = [w]

    if current:
        chunks.append(" ".join(current))

    state["chunks"] = chunks
    return state


def generate_summaries_node(state: State) -> State:
    """
    Node 2: Generate a tiny summary for each chunk.
    Very naive: take first sentence or first 50 characters.
    """
    chunks: List[str] = state.get("chunks", [])
    summaries: List[str] = []

    for chunk in chunks:
        parts = [s.strip() for s in chunk.split(".") if s.strip()]
        if parts:
            summaries.append(parts[0])
        else:
            summaries.append(chunk[:50])

    state["summaries"] = summaries
    return state


def merge_summaries_node(state: State) -> State:
    """
    Node 3: Merge all chunk summaries into one long summary.
    """
    summaries: List[str] = state.get("summaries", [])
    merged = " ".join(summaries)

    state["merged_summary"] = merged
    state["summary"] = merged
    state["summary_length"] = len(merged)
    return state


def refine_summary_node(state: State) -> State:
    """
    Node 4: Refine final summary until it is under max_summary_length.
    We'll run this node in a loop using the graph edges.
    """
    summary = state.get("summary", "")
    max_length = state.get("max_summary_length", 200)

    if len(summary) <= max_length:
        state["summary_length"] = len(summary)
        return state

    truncated = summary[:max_length]

    # Try to cut nicely at the last period if it's reasonably far inside
    last_dot = truncated.rfind(".")
    if last_dot != -1 and last_dot > max_length * 0.5:
        truncated = truncated[: last_dot + 1]

    state["summary"] = truncated.strip()
    state["summary_length"] = len(state["summary"])
    return state


# Register these nodes into the global node registry
register_node("split_text", split_text_node)
register_node("generate_summaries", generate_summaries_node)
register_node("merge_summaries", merge_summaries_node)
register_node("refine_summary", refine_summary_node)
