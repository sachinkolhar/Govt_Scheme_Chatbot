import { apiFetch, authHeaders } from "@/services/api";
import type { EligibilityRequest, Scheme } from "@/lib/types/schemes";

export function findEligibleSchemes(payload: EligibilityRequest) {
  return apiFetch<Scheme[]>("/api/find-eligible", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function getRecommendations(token: string, topK = 6) {
  return apiFetch<Scheme[]>(`/api/recommendations?top_k=${topK}`, {
    headers: authHeaders(token),
  });
}

export function addToFavorites(
  token: string,
  schemeId: string,
  schemeName: string,
) {
  return apiFetch<{ message: string }>(
    `/api/favorites/${schemeId}?scheme_name=${encodeURIComponent(schemeName)}`,
    {
      method: "POST",
      headers: authHeaders(token),
    },
  );
}

export function removeFromFavorites(token: string, schemeId: string) {
  return apiFetch<{ message: string }>(`/api/favorites/${schemeId}`, {
    method: "DELETE",
    headers: authHeaders(token),
  });
}

export function getFavorites(token: string) {
  return apiFetch<{ schemes: Scheme[]; total_count: number }>(
    `/api/favorites`,
    {
      headers: authHeaders(token),
    },
  );
}
