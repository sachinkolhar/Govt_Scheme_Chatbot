"use client";

import { chatApi } from "@/lib/api";
import type { ChatRequest } from "@/lib/types/chat";

export function useChatStream() {
  return {
    streamChat: (payload: ChatRequest) => chatApi.streamChat(payload),
  };
}
