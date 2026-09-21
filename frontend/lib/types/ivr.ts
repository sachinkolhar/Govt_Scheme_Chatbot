// IVR types and interfaces.

export interface IVRScheme {
  scheme_name: string;
  summary: string;
  benefits: string[];
  eligibility: string[];
  documents: string[];
  application_process: string[];
  level: string;
  category: string;
  state: string;
}

export interface TranslateRequest {
  text: string;
  language: string;
}

export interface TranslateResponse {
  original_text: string;
  translated_text: string;
  language: string;
}

export interface SpeakRequest {
  text: string;
  language: string;
}

export interface SpeakResponse {
  audio: string;  // base64-encoded audio data
  language: string;
  text: string;
  format: string;
  success?: boolean;
  error?: string;
}

export type IVRLanguage = "english" | "kannada" | "hindi" | "telugu" | "tamil";

export interface IVRCallState {
  isActive: boolean;
  language: IVRLanguage | null;
  currentSection: "greeting" | "language" | "summary" | "menu" | "section" | "ended";
  isPlaying: boolean;
  isMuted: boolean;
  volume: number;
  elapsedSeconds: number;
}

export interface PhoneKeypadEvent {
  key: string;
  timestamp: number;
}
