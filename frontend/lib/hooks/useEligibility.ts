"use client";

import { useCallback, useState } from "react";
import { schemesApi } from "@/lib/api";
import type { EligibilityRequest, Scheme } from "@/lib/types/schemes";

export function useEligibility() {
  const [eligible, setEligible] = useState<Scheme[]>([]);
  const [eligibleLoading, setEligibleLoading] = useState(false);

  const findEligible = useCallback(async (payload: EligibilityRequest) => {
    setEligibleLoading(true);
    try {
      setEligible(await schemesApi.findEligibleSchemes(payload));
    } catch {
      setEligible([]);
    } finally {
      setEligibleLoading(false);
    }
  }, []);

  return { eligible, setEligible, eligibleLoading, findEligible };
}
