import { apiFetch } from "@/services/api";
import type {
  SpeechRequest,
  SpeechResponse,
  VoiceChatRequest,
  VoiceChatResponse,
  VoiceEligibilityCriteriaResponse,
} from "@/lib/types/voice";

export function synthesizeSpeech(payload: SpeechRequest) {
  return apiFetch<SpeechResponse>("/api/audio/synthesize", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function transcribeSpeech(payload: SpeechRequest) {
  return apiFetch<SpeechResponse>("/api/audio/transcribe", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function askVoiceAssistant(payload: VoiceChatRequest) {
  return apiFetch<VoiceChatResponse>("/api/voice-assistant/chat", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function getVoiceEligibilityCriteria(
  schemeName: string,
  language: string,
) {
  return apiFetch<VoiceEligibilityCriteriaResponse>(
    "/api/voice-assistant/eligibility-criteria",
    {
      method: "POST",
      body: JSON.stringify({ scheme_name: schemeName, language }),
    },
  );
}
