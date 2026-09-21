"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import MicButton from "@/components/MicButton";
import * as audioApi from "@/lib/audioApi";
import { useAuthSession } from "@/lib/useAuthSession";

type LanguageCode = "en" | "hi" | "te" | "ta";
type VoiceState =
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

interface VoiceChatResponse {
  query: string;
  answer: string;
  language: string;
}

interface VoiceHistoryMessage {
  role: "user" | "assistant";
  content: string;
}

interface EligibilityCriterion {
  key: string;
  label: string;
  question: string;
  expected: string;
  description?: string;
}

interface EligibilityFlow {
  schemeName: string;
  criteria: EligibilityCriterion[];
  currentIndex: number;
  responses: Record<string, string>;
}

interface EligibilityMatchResult {
  criterion: EligibilityCriterion;
  answer: string;
  matched: boolean;
  reason: string;
}

const LANGUAGE_SELECTION_PROMPTS: { language: LanguageCode; text: string }[] = [
  {
    language: "en",
    text: "If you want to continue in English, say English.",
  },
  {
    language: "hi",
    text: "अगर आप हिंदी में जारी रखना चाहते हैं, तो हिंदी कहें।",
  },
  {
    language: "te",
    text: "మీరు తెలుగులో కొనసాగాలనుకుంటే, తెలుగు అని చెప్పండి.",
  },
  {
    language: "ta",
    text: "நீங்கள் தமிழில் தொடர விரும்பினால், தமிழ் என்று சொல்லுங்கள்.",
  },
];

const LANGUAGE_SELECTION_PROMPT_TEXT = LANGUAGE_SELECTION_PROMPTS.map(
  (prompt) => prompt.text,
).join("\n");

const SCHEME_HELP_PROMPTS: Record<LanguageCode, string> = {
  en: "How can I help you regarding government schemes?",
  hi: "सरकारी योजनाओं के बारे में मैं आपकी कैसे मदद कर सकता हूँ?",
  te: "ప్రభుత్వ పథకాల గురించి నేను మీకు ఎలా సహాయం చేయగలను?",
  ta: "அரசுத் திட்டங்கள் குறித்து நான் உங்களுக்கு எப்படி உதவலாம்?",
};

const ELIGIBILITY_INTRO_PROMPTS: Record<LanguageCode, string> = {
  en: "I will check your eligibility step by step. Please answer one question at a time.",
  hi: "मैं आपकी पात्रता चरण दर चरण जांचूंगा। कृपया एक समय में एक प्रश्न का उत्तर दें।",
  te: "నేను మీ అర్హతను దశలవారీగా తనిఖీ చేస్తాను. దయచేసి ఒక్కో ప్రశ్నకు సమాధానం ఇవ్వండి.",
  ta: "உங்கள் தகுதியை படிப்படியாக சரிபார்க்கிறேன். ஒவ்வொரு கேள்விக்கும் தனித்தனியாக பதிலளிக்கவும்.",
};

const ELIGIBILITY_FALLBACK_QUESTIONS: Record<LanguageCode, EligibilityCriterion[]> = {
  en: [
    { key: "income", label: "Annual income", question: "What is your annual family income?", expected: "Annual family income should be within the scholarship income limit." },
    { key: "category", label: "Caste/category", question: "What is your caste or category?", expected: "Applicant should belong to an eligible category, if required." },
    { key: "qualification", label: "Qualification", question: "What is your current academic qualification?", expected: "Applicant should be a student with the required academic qualification." },
    { key: "age", label: "Age", question: "What is your age?", expected: "Applicant should satisfy the scholarship age limit, if specified." },
    { key: "state", label: "State/domicile", question: "Which state is your domicile or permanent residence?", expected: "Applicant should satisfy the state or domicile requirement." },
  ],
  hi: [
    { key: "income", label: "वार्षिक आय", question: "आपके परिवार की वार्षिक आय कितनी है?", expected: "परिवार की वार्षिक आय छात्रवृत्ति की आय सीमा के भीतर होनी चाहिए।" },
    { key: "category", label: "जाति/श्रेणी", question: "आपकी जाति या श्रेणी क्या है?", expected: "यदि आवश्यक हो, आवेदक योग्य श्रेणी से होना चाहिए।" },
    { key: "qualification", label: "शैक्षणिक योग्यता", question: "आपकी वर्तमान शैक्षणिक योग्यता क्या है?", expected: "आवेदक आवश्यक शैक्षणिक योग्यता वाला विद्यार्थी होना चाहिए।" },
    { key: "age", label: "आयु", question: "आपकी उम्र कितनी है?", expected: "आवेदक छात्रवृत्ति की आयु सीमा को पूरा करना चाहिए, यदि दी गई हो।" },
    { key: "state", label: "राज्य/निवास", question: "आपका डोमिसाइल या स्थायी निवास किस राज्य में है?", expected: "आवेदक को राज्य या डोमिसाइल शर्त पूरी करनी चाहिए।" },
  ],
  te: [
    { key: "income", label: "వార్షిక ఆదాయం", question: "మీ కుటుంబ వార్షిక ఆదాయం ఎంత?", expected: "కుటుంబ వార్షిక ఆదాయం స్కాలర్‌షిప్ ఆదాయ పరిమితిలో ఉండాలి." },
    { key: "category", label: "కులం/వర్గం", question: "మీ కులం లేదా వర్గం ఏమిటి?", expected: "అవసరమైతే, అభ్యర్థి అర్హత గల వర్గానికి చెందినవారు కావాలి." },
    { key: "qualification", label: "విద్యార్హత", question: "మీ ప్రస్తుత విద్యార్హత ఏమిటి?", expected: "అభ్యర్థి అవసరమైన విద్యార్హతతో విద్యార్థి కావాలి." },
    { key: "age", label: "వయస్సు", question: "మీ వయస్సు ఎంత?", expected: "సూచించినట్లయితే, అభ్యర్థి వయస్సు పరిమితిని తీర్చాలి." },
    { key: "state", label: "రాష్ట్రం/నివాసం", question: "మీ డొమిసైల్ లేదా శాశ్వత నివాస రాష్ట్రం ఏది?", expected: "అభ్యర్థి రాష్ట్రం లేదా డొమిసైల్ షరతును తీర్చాలి." },
  ],
  ta: [
    { key: "income", label: "ஆண்டு வருமானம்", question: "உங்கள் குடும்ப ஆண்டு வருமானம் எவ்வளவு?", expected: "குடும்ப ஆண்டு வருமானம் கல்வித்தொகை வருமான வரம்புக்குள் இருக்க வேண்டும்." },
    { key: "category", label: "சாதி/வகை", question: "உங்கள் சாதி அல்லது வகை என்ன?", expected: "தேவைப்பட்டால், விண்ணப்பதாரர் தகுதியான வகையைச் சேர்ந்தவராக இருக்க வேண்டும்." },
    { key: "qualification", label: "கல்வித் தகுதி", question: "உங்கள் தற்போதைய கல்வித் தகுதி என்ன?", expected: "விண்ணப்பதாரர் தேவையான கல்வித் தகுதியுள்ள மாணவராக இருக்க வேண்டும்." },
    { key: "age", label: "வயது", question: "உங்கள் வயது என்ன?", expected: "குறிப்பிட்டிருந்தால், விண்ணப்பதாரர் வயது வரம்பை பூர்த்தி செய்ய வேண்டும்." },
    { key: "state", label: "மாநிலம்/வசிப்பிடம்", question: "உங்கள் நிரந்தர வசிப்பிடம் அல்லது டொமிசைல் மாநிலம் எது?", expected: "விண்ணப்பதாரர் மாநிலம் அல்லது டொமிசைல் நிபந்தனையை பூர்த்தி செய்ய வேண்டும்." },
  ],
};

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
  const [eligibilityFlow, setEligibilityFlow] =
    useState<EligibilityFlow | null>(null);
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
    setVoiceSupported(
      audioApi.isBrowserSpeechRecognitionSupported() ||
        audioApi.isMediaRecorderSupported(),
    );
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

  function isEligibilityCheckQuery(query: string) {
    const text = query.toLowerCase();
    return [
      "eligibility",
      "eligible",
      "am i eligible",
      "check my eligibility",
      "पात्र",
      "योग्य",
      "అర్హ",
      "தகுதி",
    ].some((phrase) => text.includes(phrase));
  }

  function extractSchemeName(query: string) {
    const cleaned = query
      .replace(/[?.!,]/g, " ")
      .replace(/\s+/g, " ")
      .trim();
    const lower = cleaned.toLowerCase();
    const forMatch = cleaned.match(/\bfor\s+(.+)$/i);
    if (forMatch?.[1]) {
      return forMatch[1]
        .replace(/\b(scheme|scholarship)\b$/i, "$1")
        .trim();
    }
    const patterns = [
      "check my eligibility",
      "am i eligible for",
      "am i eligible",
      "eligible for",
      "eligibility for",
      "eligibility",
      "this scheme",
      "this scholarship",
    ];
    let result = cleaned;
    for (const pattern of patterns) {
      result = result.replace(new RegExp(pattern, "ig"), " ");
    }
    result = result.replace(/\s+/g, " ").trim();
    if (!result || lower.includes("this scheme")) {
      return "this scholarship scheme";
    }
    return result;
  }

  async function fetchEligibilityCriteria(schemeName: string) {
    const response = await fetch("/api/voice-assistant/eligibility-criteria", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        scheme_name: schemeName,
        language: voiceLanguage,
      }),
    });
    if (!response.ok) {
      return ELIGIBILITY_FALLBACK_QUESTIONS[voiceLanguage];
    }
    const data = (await response.json()) as {
      criteria?: EligibilityCriterion[];
    };
    return data.criteria?.length
      ? data.criteria
      : ELIGIBILITY_FALLBACK_QUESTIONS[voiceLanguage];
  }

  function parseSpokenNumber(text: string) {
    const normalized = text.toLowerCase().replace(/,/g, "");
    const match = normalized.match(/(\d+(?:\.\d+)?)/);
    if (!match) return null;
    let value = Number(match[1]);
    if (Number.isNaN(value)) return null;
    if (normalized.includes("crore")) value *= 10000000;
    else if (normalized.includes("lakh") || normalized.includes("lac")) value *= 100000;
    else if (normalized.includes("thousand")) value *= 1000;
    return value;
  }

  function expectedLimit(expected: string) {
    const normalized = expected.toLowerCase().replace(/,/g, "");
    const match = normalized.match(/(\d+(?:\.\d+)?)/);
    if (!match) return null;
    let value = Number(match[1]);
    if (Number.isNaN(value)) return null;
    if (normalized.includes("crore")) value *= 10000000;
    else if (normalized.includes("lakh") || normalized.includes("lac")) value *= 100000;
    else if (normalized.includes("thousand")) value *= 1000;
    return value;
  }

  function evaluateCriterion(
    criterion: EligibilityCriterion,
    answer: string,
  ): EligibilityMatchResult {
    const key = criterion.key.toLowerCase();
    const response = answer.trim().toLowerCase();
    const expected = `${criterion.expected} ${criterion.description || ""}`.toLowerCase();
    let matched = response.length > 0;

    if (key.includes("income")) {
      const answerValue = parseSpokenNumber(response);
      const limit = expectedLimit(expected);
      matched = answerValue !== null && limit !== null ? answerValue <= limit : response.length > 0;
    } else if (key.includes("age")) {
      const age = parseSpokenNumber(response);
      const limit = expectedLimit(expected);
      matched = age !== null && limit !== null ? age <= limit : response.length > 0;
    } else if (key.includes("category") || key.includes("caste")) {
      const categories = ["sc", "st", "obc", "minority", "general", "ews"];
      const expectedCategories = categories.filter((category) =>
        expected.includes(category),
      );
      matched = expectedCategories.length
        ? expectedCategories.some((category) => response.includes(category))
        : response.length > 0 && !["no", "none", "not applicable"].includes(response);
    } else if (key.includes("qualification") || key.includes("academic")) {
      matched = response.length > 0 && !["no", "none"].includes(response);
    } else if (key.includes("state") || key.includes("domicile")) {
      matched = response.length > 0 && !["no", "none"].includes(response);
    }

    return {
      criterion,
      answer,
      matched,
      reason: matched ? "Matched" : "Not matched",
    };
  }

  function buildEligibilityResultMessage(
    schemeName: string,
    results: EligibilityMatchResult[],
  ) {
    const total = results.length;
    const matched = results.filter((result) => result.matched);
    const unmatched = results.filter((result) => !result.matched);
    const matchedLabels = matched.map((result) => result.criterion.label).join(", ");
    const unmatchedLabels = unmatched.map((result) => result.criterion.label).join(", ");

    if (voiceLanguage === "hi") {
      return (
        `आप ${schemeName} के लिए ${total} में से ${matched.length} पात्रता शर्तें पूरी करते हैं।\n` +
        `✔️ पूरी हुई शर्तें: ${matchedLabels || "कोई नहीं"}.\n` +
        `❌ पूरी नहीं हुई शर्तें: ${unmatchedLabels || "कोई नहीं"}.`
      );
    }

    return (
      `You meet ${matched.length} out of ${total} eligibility criteria for ${schemeName}.\n` +
      `✔️ Matched: ${matchedLabels || "None"}.\n` +
      `❌ Not matched: ${unmatchedLabels || "None"}.`
    );
  }

  async function startEligibilityFlow(queryText: string) {
    const schemeName = extractSchemeName(queryText);
    setVoiceState("FETCHING_ELIGIBILITY");
    setStatusMessage(`Fetching eligibility criteria for ${schemeName}...`);
    setVoiceError("");

    const criteria = await fetchEligibilityCriteria(schemeName);
    const flow: EligibilityFlow = {
      schemeName,
      criteria,
      currentIndex: 0,
      responses: {},
    };
    setEligibilityFlow(flow);

    const firstQuestion = criteria[0]?.question;
    if (!firstQuestion) {
      throw new Error("No eligibility questions were found.");
    }
    const prompt = `${ELIGIBILITY_INTRO_PROMPTS[voiceLanguage]}\n\n${firstQuestion}`;
    setAssistantResponse(prompt);
    setVoiceState("SPEAKING_RESPONSE");
    setStatusMessage("Asking eligibility question...");
    await speakAssistantMessage(prompt);
    setVoiceState("ASKING_ELIGIBILITY");
    setStatusMessage("Listening for eligibility answer...");
  }

  async function processEligibilityAnswer(answer: string) {
    if (!eligibilityFlow) return;
    const criterion = eligibilityFlow.criteria[eligibilityFlow.currentIndex];
    if (!criterion) return;

    const responses = {
      ...eligibilityFlow.responses,
      [criterion.key]: answer,
    };
    const nextIndex = eligibilityFlow.currentIndex + 1;
    const nextCriterion = eligibilityFlow.criteria[nextIndex];

    if (nextCriterion) {
      const nextFlow = {
        ...eligibilityFlow,
        currentIndex: nextIndex,
        responses,
      };
      setEligibilityFlow(nextFlow);
      setAssistantResponse(nextCriterion.question);
      setVoiceState("SPEAKING_RESPONSE");
      setStatusMessage("Asking next eligibility question...");
      await speakAssistantMessage(nextCriterion.question);
      setVoiceState("ASKING_ELIGIBILITY");
      setStatusMessage("Listening for eligibility answer...");
      return;
    }

    const completedFlow = {
      ...eligibilityFlow,
      responses,
    };
    const results = completedFlow.criteria.map((item) =>
      evaluateCriterion(item, responses[item.key] || ""),
    );
    const finalMessage = buildEligibilityResultMessage(
      completedFlow.schemeName,
      results,
    );
    setEligibilityFlow(completedFlow);
    setAssistantResponse(finalMessage);
    setVoiceState("SPEAKING_RESPONSE");
    setStatusMessage("Speaking eligibility result...");
    await speakAssistantMessage(finalMessage);
    setVoiceState("LANGUAGE_SELECTED");
    setStatusMessage("Ready for your next question");
  }

  async function speakAssistantMessage(text: string, language = voiceLanguage) {
    setAssistantSpeaking(text);
    setIsSpeaking(true);
    try {
      console.log(
        `[Voice] Speaking response (${language}): ${text.substring(0, 50)}...`,
      );
      const result = await audioApi.synthesizeAndPlayAudio(text, language);
      console.log(`[Voice] Speech result:`, result);
      if (!result.success) {
        console.error(`[Voice] Audio playback failed: ${result.error}`);
        setVoiceError(result.error || "Failed to play audio");
      }
    } catch (err) {
      const msg = err instanceof Error ? err.message : "Failed to play audio";
      console.error(`[Voice] Exception during speech:`, err);
      setVoiceError(msg);
    } finally {
      setIsSpeaking(false);
      setAssistantSpeaking("");
    }
  }

  async function speakLanguageSelectionPrompt() {
    setAssistantSpeaking(LANGUAGE_SELECTION_PROMPT_TEXT);
    setIsSpeaking(true);
    try {
      for (const prompt of LANGUAGE_SELECTION_PROMPTS) {
        const result = await audioApi.synthesizeAndPlayAudio(
          prompt.text,
          prompt.language,
        );
        if (!result.success) {
          setVoiceError(result.error || "Failed to play language prompt");
        }
      }
    } catch (err) {
      const msg =
        err instanceof Error ? err.message : "Failed to play language prompt";
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

    await speakAssistantMessage(
      SCHEME_HELP_PROMPTS[detectedLanguage],
      detectedLanguage,
    );

    // Transition to listening for query
    setVoiceState("LISTENING_QUERY");
    setStatusMessage("Listening for your question...");
  }

  async function processSchemeQuery(queryText: string) {
    console.log(`[Voice] Processing query: ${queryText}`);
    setUserQueryTranscript(queryText);
    setVoiceState("PROCESSING");
    setStatusMessage("Processing your query...");
    setVoiceError("");

    try {
      if (isEligibilityCheckQuery(queryText)) {
        await startEligibilityFlow(queryText);
        return;
      }

      console.log(
        `[Voice] Calling voice assistant for language: ${voiceLanguage}`,
      );
      const response = await askSchemeAssistant(queryText);
      console.log(
        `[Voice] Received response length: ${response.answer?.length || 0} chars`,
      );
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
      console.log(`[Voice] Transitioning to SPEAKING_RESPONSE state`);
      setVoiceState("SPEAKING_RESPONSE");
      setStatusMessage("Speaking response...");

      console.log(`[Voice] Starting audio playback`);
      await speakAssistantMessage(
        response.answer || "I could not find an answer.",
      );

      console.log(`[Voice] Audio playback completed, ready for next query`);
      setVoiceState("LANGUAGE_SELECTED");
      setStatusMessage("Ready for your next question");
    } catch (err) {
      const msg =
        err instanceof Error ? err.message : "Voice assistant request failed";
      console.error(`[Voice] Error in processSchemeQuery:`, err);
      setVoiceError(msg);
      setVoiceState("IDLE");
      setStatusMessage("Error occurred. Ready to start again.");
    }
  }

  async function handleMicTranscript(text: string) {
    const clean = text.trim();
    if (!clean) return;

    setVoiceError("");

    if (voiceState === "ASKING_ELIGIBILITY") {
      await processEligibilityAnswer(clean);
      return;
    }

    if (voiceState === "IDLE" || voiceState === "LISTENING_LANGUAGE") {
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

    if (voiceState === "LANGUAGE_SELECTED" || voiceState === "LISTENING_QUERY") {
      await processSchemeQuery(clean);
      return;
    }
  }

  async function prepareMicInteraction() {
    if (voiceState === "IDLE") {
      setVoiceState("ASKING_LANGUAGE");
      setVoiceLanguage("en");
      setStatusMessage("Asking you to choose a language...");
      setUserLanguageTranscript("");
      setUserQueryTranscript("");
      setAssistantResponse("");
      setAssistantSpeaking("");
      setVoiceError("");
      setVoiceHistory([]);
      setEligibilityFlow(null);
      await speakLanguageSelectionPrompt();
      setVoiceState("LISTENING_LANGUAGE");
      setStatusMessage(
        "Listening for language (say: English, Hindi, Telugu, or Tamil)...",
      );
      return;
    }

    if (voiceState === "LANGUAGE_SELECTED") {
      setVoiceState("LISTENING_QUERY");
      setStatusMessage("Listening for your question...");
      return;
    }

    if (voiceState === "ASKING_ELIGIBILITY") {
      setStatusMessage("Listening for eligibility answer...");
    }
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
              onBeforeStart={prepareMicInteraction}
              onTranscript={(text) => void handleMicTranscript(text)}
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

        {eligibilityFlow && (
          <section className="bg-white rounded-2xl border border-orange-100 shadow-sm p-6">
            <h2 className="text-xl font-bold text-gray-800">
              Eligibility Check
            </h2>
            <div className="mt-3 text-sm text-gray-700">
              Scheme: {eligibilityFlow.schemeName}
            </div>
            <div className="mt-4 space-y-2">
              {eligibilityFlow.criteria.map((criterion, index) => (
                <div
                  key={`${criterion.key}-${index}`}
                  className="rounded-lg border border-gray-200 bg-gray-50 px-3 py-2"
                >
                  <div className="text-sm font-semibold text-gray-800">
                    {index + 1}. {criterion.label}
                  </div>
                  <div className="text-xs text-gray-600 mt-1">
                    {criterion.question}
                  </div>
                  {eligibilityFlow.responses[criterion.key] && (
                    <div className="text-xs text-green-700 mt-1">
                      Answer: {eligibilityFlow.responses[criterion.key]}
                    </div>
                  )}
                </div>
              ))}
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
