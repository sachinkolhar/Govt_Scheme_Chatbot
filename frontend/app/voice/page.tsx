"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import MicButton from "@/components/MicButton";
import * as audioApi from "@/lib/audioApi";
import { useAuthSession } from "@/lib/useAuthSession";

type LanguageCode = "en" | "hi" | "te" | "ta";
type VoiceState =
  | "IDLE"
  | "LISTENING_LANGUAGE"
  | "LANGUAGE_SELECTED"
  | "LISTENING_QUERY"
  | "PROCESSING"
  | "SPEAKING_RESPONSE";

interface VoiceChatResponse {
  query: string;
  answer: string;
  language: string;
}

interface VoiceHistoryMessage {
  role: "user" | "assistant";
  content: string;
}

const LANGUAGE_SELECTION_PROMPT =
  "Can you please choose your preferred language?";
const SCHEME_HELP_PROMPT = "How can I help you regarding government schemes?";

export default function VoicePage() {
  const { token, user, sessionLoading, clearSession } = useAuthSession();
  const [voiceState, setVoiceState] = useState<VoiceState>("IDLE");
  const [voiceLanguage, setVoiceLanguage] = useState<LanguageCode>("en");
  const [voiceSupported, setVoiceSupported] = useState(false);
  const [userLanguageTranscript, setUserLanguageTranscript] = useState("");
  const [userQueryTranscript, setUserQueryTranscript] = useState("");
  const [assistantResponse, setAssistantResponse] = useState("");
  const [assistantSpeaking, setAssistantSpeaking] = useState("");
  const [voiceHistory, setVoiceHistory] = useState<VoiceHistoryMessage[]>([]);
  const [voiceError, setVoiceError] = useState("");
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [statusMessage, setStatusMessage] = useState("Ready to start");
  // Legacy state variables for backward compatibility (will be removed)
  const [voiceStep] = useState<"language_selection" | "scheme_query">(
    "language_selection",
  );
  const [transcript] = useState("");
  const [assistantAnswer] = useState("");
  const [queryLoading] = useState(false);
  const [voicePrompt] = useState("");

  const languageNames: Record<LanguageCode, string> = {
    en: "English",
    hi: "हिंदी",
    te: "తెలుగు",
    ta: "தமிழ்",
  };

  const greetingName = useMemo(() => user?.name || "Citizen", [user]);

  useEffect(() => {
    const speechRecognition =
      (window as any).SpeechRecognition ||
      (window as any).webkitSpeechRecognition;
    const canSpeak =
      typeof window !== "undefined" && "speechSynthesis" in window;
    setVoiceSupported(Boolean(speechRecognition || canSpeak));
  }, []);

  function detectLanguageFromTranscript(rawText: string): LanguageCode | null {
    const text = rawText.trim().toLowerCase();
    if (!text) return null;

    const languageHints: Record<LanguageCode, string[]> = {
      en: ["english", "eng", "inglish"],
      hi: ["hindi", "hind", "हिंदी", "हिन्दी"],
      te: ["telugu", "తెలుగు"],
      ta: ["tamil", "தமிழ்", "thamizh"],
    };

    for (const [code, hints] of Object.entries(languageHints) as [
      LanguageCode,
      string[],
    ][]) {
      if (hints.some((hint) => text.includes(hint))) {
        return code;
      }
    }

    return null;
  }

  async function askSchemeAssistant(query: string): Promise<VoiceChatResponse> {
    const response = await fetch("/api/voice-assistant/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        query,
        language: voiceLanguage,
        history: voiceHistory,
      }),
    });

    if (!response.ok) {
      const raw = await response.text();
      throw new Error(raw || "Voice assistant request failed");
    }

    return (await response.json()) as VoiceChatResponse;
  }

  async function speakAssistantMessage(text: string) {
    setAssistantSpeaking(text);
    setIsSpeaking(true);
    try {
      const result = await audioApi.synthesizeAndPlayAudio(text, voiceLanguage);
      if (!result.success) {
        setVoiceError(result.error || "Failed to play audio");
      }
    } catch (err) {
      const msg = err instanceof Error ? err.message : "Failed to play audio";
      setVoiceError(msg);
    } finally {
      setIsSpeaking(false);
      setAssistantSpeaking("");
    }
  }

  async function processLanguageSelection(detectedLanguage: LanguageCode) {
    setVoiceLanguage(detectedLanguage);
    setVoiceState("LANGUAGE_SELECTED");
    setStatusMessage(`Language selected: ${languageNames[detectedLanguage]}`);
    setAssistantResponse("");
    setVoiceHistory([]);

    // Speak the scheme help prompt
    await speakAssistantMessage(SCHEME_HELP_PROMPT);

    // Transition to listening for query
    setVoiceState("LISTENING_QUERY");
    setStatusMessage("Listening for your question...");
  }

  async function processSchemeQuery(queryText: string) {
    setUserQueryTranscript(queryText);
    setVoiceState("PROCESSING");
    setStatusMessage("Processing your query...");
    setVoiceError("");

    try {
      const response = await askSchemeAssistant(queryText);
      setAssistantResponse(response.answer || "I could not find an answer.");
      setVoiceHistory((prev) => {
        const next = [
          ...prev,
          { role: "user" as const, content: queryText },
          { role: "assistant" as const, content: response.answer || "" },
        ];
        return next.slice(-8);
      });

      // Transition to speaking response
      setVoiceState("SPEAKING_RESPONSE");
      setStatusMessage("Speaking response...");
      await speakAssistantMessage(
        response.answer || "I could not find an answer.",
      );

      // Return to idle after speaking
      setVoiceState("IDLE");
      setStatusMessage("Ready to start a new query");
    } catch (err) {
      const msg =
        err instanceof Error ? err.message : "Voice assistant request failed";
      setVoiceError(msg);
      setVoiceState("IDLE");
      setStatusMessage("Error occurred. Ready to start again.");
    }
  }

  async function handleMicTranscript(text: string) {
    const clean = text.trim();
    if (!clean) return;

    setVoiceError("");

    if (voiceState === "LISTENING_LANGUAGE") {
      setUserLanguageTranscript(clean);
      const detectedLanguage = detectLanguageFromTranscript(clean);
      if (!detectedLanguage) {
        setVoiceError(
          "Could not detect language. Please say: English, Hindi, Telugu, or Tamil.",
        );
        setVoiceState("LISTENING_LANGUAGE");
        setStatusMessage(
          "Listening for language (say: English, Hindi, Telugu, or Tamil)...",
        );
        return;
      }

      await processLanguageSelection(detectedLanguage);
      return;
    }

    if (voiceState === "LISTENING_QUERY") {
      await processSchemeQuery(clean);
      return;
    }
  }

  function startVoiceFlow() {
    setVoiceState("LISTENING_LANGUAGE");
    setStatusMessage("Listening for language...");
    setUserLanguageTranscript("");
    setUserQueryTranscript("");
    setAssistantResponse("");
    setAssistantSpeaking("");
    setVoiceError("");
  }

  function logout() {
    clearSession();
  }

  if (sessionLoading) {
    return (
      <main className="min-h-screen bg-gradient-to-br from-orange-50 via-white to-green-50 flex items-center justify-center p-4">
        <section className="w-full max-w-lg bg-white rounded-2xl border border-orange-100 shadow-xl p-7 text-center">
          <p className="text-sm text-gray-500">Loading session...</p>
        </section>
      </main>
    );
  }

  if (!token || !user) {
    return (
      <main className="min-h-screen bg-gradient-to-br from-orange-50 via-white to-green-50 flex items-center justify-center p-4">
        <section className="w-full max-w-lg bg-white rounded-2xl border border-orange-100 shadow-xl p-7 text-center">
          <h1 className="text-2xl font-extrabold text-gray-800">
            Voice Assistant
          </h1>
          <p className="text-sm text-gray-500 mt-2">
            Login from the main page to use voice features.
          </p>
          <Link
            href="/"
            className="mt-5 inline-flex items-center justify-center rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium hover:bg-gray-50"
          >
            Back To Main
          </Link>
        </section>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-orange-50 via-white to-green-50">
      <header className="border-b border-orange-100 bg-white/90 backdrop-blur-sm sticky top-0 z-10">
        <div className="max-w-4xl mx-auto px-4 py-5 flex items-center justify-between gap-3">
          <div>
            <h1 className="text-2xl font-extrabold text-gray-800">
              Voice Assistant
            </h1>
            <p className="text-sm text-gray-500">
              Hello {greetingName} - dedicated voice-driven assistant
            </p>
          </div>
          <div className="flex items-center gap-2">
            <Link
              href="/"
              className="text-sm px-4 py-2 rounded-lg border border-gray-300 hover:bg-gray-50"
            >
              Back To Chat
            </Link>
            <button
              onClick={logout}
              className="text-sm px-4 py-2 rounded-lg border border-gray-300 hover:bg-gray-50"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      <section className="max-w-4xl mx-auto px-4 py-8 space-y-6">
        {/* Voice Control Section */}
        <section className="bg-white rounded-2xl border border-orange-100 shadow-sm p-6">
          <h2 className="text-xl font-bold text-gray-800">Voice Control</h2>
          <p className="text-sm text-gray-500 mt-1">
            Click the Mic button to start the complete voice interaction flow
          </p>

          {/* Status Display */}
          <div className="mt-4 rounded-lg border border-blue-200 bg-blue-50 px-4 py-3">
            <div className="text-sm font-semibold text-blue-900">
              Status: {statusMessage}
            </div>
            {voiceState !== "IDLE" && (
              <div className="text-xs text-blue-700 mt-1">
                State: {voiceState}
              </div>
            )}
          </div>

          {/* Mic Button - Single Control */}
          <div className="mt-6 flex justify-center">
            <MicButton
              language={voiceLanguage}
              onTranscript={(text) => {
                if (voiceState === "IDLE") {
                  startVoiceFlow();
                }
                void handleMicTranscript(text);
              }}
              onError={(error) => setVoiceError(error)}
              disabled={!voiceSupported || isSpeaking}
            />
          </div>

          {/* Instructions */}
          {voiceState === "IDLE" && (
            <div className="mt-4 text-center">
              <p className="text-sm text-gray-600">
                Click the Mic button above to start. The assistant will guide
                you through:
              </p>
              <ol className="text-xs text-gray-600 mt-2 space-y-1">
                <li>1. Select your preferred language</li>
                <li>2. Ask about government schemes</li>
                <li>3. Receive voice response with answers</li>
              </ol>
            </div>
          )}
        </section>

        {/* Transcript Section */}
        {(userLanguageTranscript || userQueryTranscript) && (
          <section className="bg-white rounded-2xl border border-orange-100 shadow-sm p-6">
            <h2 className="text-xl font-bold text-gray-800">
              Conversation Transcript
            </h2>
            <div className="mt-4 space-y-3">
              {userLanguageTranscript && (
                <div className="border-l-4 border-blue-500 bg-blue-50 p-3">
                  <div className="text-xs font-semibold text-blue-900 mb-1">
                    User (Language Selection):
                  </div>
                  <div className="text-sm text-blue-800">
                    {userLanguageTranscript}
                  </div>
                  <div className="text-xs text-blue-600 mt-1">
                    Selected: {languageNames[voiceLanguage]}
                  </div>
                </div>
              )}
              {userQueryTranscript && (
                <div className="border-l-4 border-green-500 bg-green-50 p-3">
                  <div className="text-xs font-semibold text-green-900 mb-1">
                    User (Query):
                  </div>
                  <div className="text-sm text-green-800">
                    {userQueryTranscript}
                  </div>
                </div>
              )}
            </div>
          </section>
        )}

        {/* Assistant Speaking Section */}
        {assistantSpeaking && (
          <section className="bg-white rounded-2xl border border-purple-100 shadow-sm p-6">
            <h2 className="text-xl font-bold text-gray-800">
              Assistant Speaking
            </h2>
            <div className="mt-4 rounded-lg border border-purple-200 bg-purple-50 px-4 py-3">
              <div className="text-sm text-purple-900 italic">
                "{assistantSpeaking}"
              </div>
            </div>
          </section>
        )}

        {/* Assistant Response Section */}
        {assistantResponse && (
          <section className="bg-white rounded-2xl border border-orange-100 shadow-sm p-6">
            <h2 className="text-xl font-bold text-gray-800">
              Assistant Response
            </h2>
            <div className="mt-4 rounded-lg border border-gray-200 bg-gray-50 px-4 py-3">
              <div className="text-sm text-gray-800 whitespace-pre-wrap leading-relaxed">
                {assistantResponse}
              </div>
            </div>
            <div className="mt-3 text-xs text-gray-500">
              Language: {languageNames[voiceLanguage]}
            </div>
          </section>
        )}

        {/* Error Section */}
        {voiceError && (
          <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-sm text-red-700">
            <div className="font-semibold mb-1">Error:</div>
            {voiceError}
            <button
              onClick={() => setVoiceError("")}
              className="ml-2 underline hover:no-underline text-red-600"
            >
              Dismiss
            </button>
          </div>
        )}
      </section>
    </main>
  );
}
