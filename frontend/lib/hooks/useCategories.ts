"use client";

import { useCallback, useState } from "react";
import { searchApi } from "@/lib/api";
import type { CategorySummary } from "@/lib/types/schemes";

export function useCategories() {
  const [categories, setCategories] = useState<CategorySummary[]>([]);

  const loadCategories = useCallback(async () => {
    try {
      setCategories(await searchApi.getCategories());
    } catch {
      setCategories([]);
    }
  }, []);

  return { categories, setCategories, loadCategories };
}
