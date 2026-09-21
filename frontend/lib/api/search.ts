import { apiFetch } from "@/services/api";
import type { CategorySummary, Scheme } from "@/lib/types/schemes";

export function searchSchemes(query: string, topK = 5) {
  return apiFetch<{ query: string; results: Scheme[] }>("/api/search", {
    method: "POST",
    body: JSON.stringify({ query, top_k: topK }),
  });
}

export function getCategories() {
  return apiFetch<CategorySummary[]>("/api/categories");
}
