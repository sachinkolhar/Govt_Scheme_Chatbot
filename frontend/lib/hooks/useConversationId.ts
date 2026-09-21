"use client";

import { useEffect, useRef } from "react";

export function useConversationId(storageKey = "gs_conversation_id") {
  const conversationIdRef = useRef("");

  useEffect(() => {
    const saved = localStorage.getItem(storageKey);
    if (saved) {
      conversationIdRef.current = saved;
      return;
    }
    const newId =
      typeof crypto !== "undefined" && "randomUUID" in crypto
        ? crypto.randomUUID()
        : `conv-${Date.now()}-${Math.random().toString(36).slice(2, 10)}`;
    conversationIdRef.current = newId;
    localStorage.setItem(storageKey, newId);
  }, [storageKey]);

  return conversationIdRef;
}
