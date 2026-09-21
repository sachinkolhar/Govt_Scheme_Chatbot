import type { ConversationMessage, LanguageCode } from "./chat";

export type VoiceState =
  | "IDLE"
  | "ASKING_LANGUAGE"
  | "LISTENING_LANGUAGE"
  | "LANGUAGE_SELECTED"
  | "LISTENING_QUERY"
  | "PROCESSING"
  | "FETCHING_ELIGIBILITY"
  | "ASKING_ELIGIBILITY"
  | "EVALUATING_ELIGIBILITY"
  | "SPEAKING_RESPONSE";

export interface SpeechRequest {
  audio_base64?: string;
  text?: string;
  language: string;
  format?: string;
}

export interface SpeechResponse {
  success: boolean;
  data?: string;
  error?: string;
  language: string;
}

export interface VoiceChatResponse {
  query: string;
  answer: string;
  language: string;
}

export interface VoiceChatRequest {
  query: string;
  language: LanguageCode;
  history: ConversationMessage[];
}

export interface EligibilityCriterion {
  key: string;
  label: string;
  question: string;
  expected: string;
  description?: string;
}

export interface VoiceEligibilityCriteriaResponse {
  scheme_name: string;
  language: string;
  criteria: EligibilityCriterion[];
}
