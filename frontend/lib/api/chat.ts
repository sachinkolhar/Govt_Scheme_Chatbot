import { apiFetch } from "@/services/api";
import type { ChatRequest, ChatResponse } from "@/lib/types/chat";

export function sendChat(payload: ChatRequest) {
  return apiFetch<ChatResponse>("/api/chat", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function streamChat(payload: ChatRequest) {
  const response = await fetch("/api/chat/stream", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error((await response.text()) || "Chat request failed");
  }

  return response;
}
