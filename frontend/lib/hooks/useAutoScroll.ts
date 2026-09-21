"use client";

import { RefObject, useEffect } from "react";

export function useAutoScroll<T extends HTMLElement>(
  ref: RefObject<T>,
  deps: unknown[],
) {
  useEffect(() => {
    if (ref.current) {
      ref.current.scrollTop = ref.current.scrollHeight;
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);
}
