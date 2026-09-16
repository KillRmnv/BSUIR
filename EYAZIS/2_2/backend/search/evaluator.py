import math
from typing import List, Dict, Set
import io
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def calculate_precision(retrieved: Set[int], relevant: Set[int]) -> float:
    if not retrieved:
        return 0.0
    return len(retrieved & relevant) / len(retrieved)


def calculate_recall(retrieved: Set[int], relevant: Set[int]) -> float:
    if not relevant:
        return 0.0
    return len(retrieved & relevant) / len(relevant)


def calculate_fscore(precision: float, recall: float, beta: float = 1.0) -> float:
    if precision + recall == 0:
        return 0.0
    return (1 + beta**2) * (precision * recall) / (beta**2 * precision + recall)


def calculate_metrics(retrieved_ids: List[int], relevant_ids: List[int]) -> Dict:
    retrieved = set(retrieved_ids)
    relevant = set(relevant_ids)

    precision = calculate_precision(retrieved, relevant)
    recall = calculate_recall(retrieved, relevant)
    fscore = calculate_fscore(precision, recall)
    f05 = calculate_fscore(precision, recall, beta=0.5)
    f2 = calculate_fscore(precision, recall, beta=2.0)

    return {
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "fscore": round(fscore, 4),
        "fscore_05": round(f05, 4),
        "fscore_2": round(f2, 4),
        "retrieved_count": len(retrieved),
        "relevant_count": len(relevant),
        "intersection_count": len(retrieved & relevant),
    }


def evaluate_search_results(
    queries_results: List[Dict],
) -> Dict:
    all_precisions = []
    all_recalls = []
    all_fscores = []

    query_metrics = []
    for qr in queries_results:
        m = calculate_metrics(qr["retrieved_ids"], qr["relevant_ids"])
        all_precisions.append(m["precision"])
        all_recalls.append(m["recall"])
        all_fscores.append(m["fscore"])
        query_metrics.append({"query": qr["query"], "metrics": m})

    avg_precision = sum(all_precisions) / len(all_precisions) if all_precisions else 0
    avg_recall = sum(all_recalls) / len(all_recalls) if all_recalls else 0
    avg_fscore = sum(all_fscores) / len(all_fscores) if all_fscores else 0

    return {
        "average_precision": round(avg_precision, 4),
        "average_recall": round(avg_recall, 4),
        "average_fscore": round(avg_fscore, 4),
        "query_metrics": query_metrics,
    }


def plot_metrics(metrics_data: Dict) -> str:
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    queries = [qm["query"][:20] for qm in metrics_data.get("query_metrics", [])]
    precisions = [qm["metrics"]["precision"] for qm in metrics_data.get("query_metrics", [])]
    recalls = [qm["metrics"]["recall"] for qm in metrics_data.get("query_metrics", [])]
    fscores = [qm["metrics"]["fscore"] for qm in metrics_data.get("query_metrics", [])]

    x = range(len(queries))

    axes[0].bar(x, precisions, color='#2563eb', alpha=0.8)
    axes[0].set_title('Precision', fontsize=14, fontweight='bold')
    axes[0].set_ylim(0, 1.1)
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(queries, rotation=45, ha='right', fontsize=8)
    axes[0].grid(axis='y', alpha=0.3)

    axes[1].bar(x, recalls, color='#1e40af', alpha=0.8)
    axes[1].set_title('Recall', fontsize=14, fontweight='bold')
    axes[1].set_ylim(0, 1.1)
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(queries, rotation=45, ha='right', fontsize=8)
    axes[1].grid(axis='y', alpha=0.3)

    axes[2].bar(x, fscores, color='#1e3a5f', alpha=0.8)
    axes[2].set_title('F1-Score', fontsize=14, fontweight='bold')
    axes[2].set_ylim(0, 1.1)
    axes[2].set_xticks(x)
    axes[2].set_xticklabels(queries, rotation=45, ha='right', fontsize=8)
    axes[2].grid(axis='y', alpha=0.3)

    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')
