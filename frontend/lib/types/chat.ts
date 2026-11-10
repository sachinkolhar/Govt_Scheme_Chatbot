import type { Scheme } from "./schemes";

export type LanguageCode = "en" | "hi" | "te" | "ta";
export type ChatResponseType =
  | "direct_answer"
  | "no_data_prompt"
  | "relevant_schemes"
  | "clarification";

export interface ChatSource {
  title: string;
  url: string;
  source_type: string;
  retrieved_at?: string | null;
}

export interface ConversationMessage {
  role: "user" | "assistant";
  content: string;
}

export interface ChatRequest {
  query: string;
  top_k: number;
  history: ConversationMessage[];
  conversation_id: string;
  language: LanguageCode;
}

export interface ChatResponse {
  query: string;
  answer: string;
  response_type: ChatResponseType;
  source_scheme: Scheme | null;
  relevant_schemes: Scheme[];
  sources?: ChatSource[];
}

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  scheme?: Scheme;
  relevantSchemes?: Scheme[];
  responseType?: ChatResponseType;
  streaming?: boolean;
  error?: string;
  sources?: ChatSource[];
}

export type ChatStreamEvent =
  | { type: "response_type"; value: ChatResponseType }
  | { type: "token"; text: string }
  | { type: "scheme"; data: Scheme }
  | { type: "relevant_schemes"; data: Scheme[] }
  | { type: "sources"; data: ChatSource[] }
  | { type: "error"; text: string }
  | { type: "done" };
