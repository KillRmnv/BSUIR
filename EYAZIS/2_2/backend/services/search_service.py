from data.database_manager import (
    get_document_count,
    log_search,
)
from search.search_engine import SearchEngine
from search.evaluator import evaluate_search_results, plot_metrics


def search_documents(engine: SearchEngine, query: str, top_k: int = 10) -> dict:
    return engine.get_results(query, top_k)


def get_metrics(engine: SearchEngine, queries_results: list) -> dict:
    for qr in queries_results:
        if "retrieved_ids" not in qr and qr.get("query"):
            res = engine.get_results(qr["query"], top_k=10)
            qr["retrieved_ids"] = [r["id"] for r in res.get("results", [])]
    evaluation = evaluate_search_results(queries_results)
    chart_b64 = plot_metrics(evaluation)
    evaluation["chart"] = chart_b64
    return evaluation


def get_stats() -> dict:
    count = get_document_count()
    return {"document_count": count}
