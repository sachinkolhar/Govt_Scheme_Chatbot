"use client";

import { useCallback, useState } from "react";
import { schemesApi } from "@/lib/api";
import type { Scheme } from "@/lib/types/schemes";

export function useRecommendations() {
  const [recommendations, setRecommendations] = useState<Scheme[]>([]);
  const [recommendLoading, setRecommendLoading] = useState(false);

  const loadRecommendations = useCallback(async (token: string, topK = 6) => {
    setRecommendLoading(true);
    try {
      setRecommendations(await schemesApi.getRecommendations(token, topK));
    } catch {
      setRecommendations([]);
    } finally {
      setRecommendLoading(false);
    }
  }, []);

  return {
    recommendations,
    setRecommendations,
    recommendLoading,
    loadRecommendations,
  };
}
