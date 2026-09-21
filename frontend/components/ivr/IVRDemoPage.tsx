"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import type { IVRLanguage, IVRScheme } from "@/lib/types/ivr";
import {
  speakText,
  getDemoScheme,
  audioBase64ToBlob,
} from "@/lib/api/ivr";
import PhoneKeypad from "./PhoneKeypad";
import WaveformAnimation from "./WaveformAnimation";
import CallStatusPanel from "./CallStatusPanel";
import VoicePlayer from "./VoicePlayer";

type CallSection =
  | "greeting"
  | "language"
  | "summary"
  | "menu"
  | "section"
  | "ended";

const SPEECH_LANGUAGE_CODES: Record<IVRLanguage, string> = {
  english: "en-IN",
  kannada: "kn-IN",
  hindi: "hi-IN",
  telugu: "te-IN",
  tamil: "ta-IN",
};

const WELCOME_SEGMENTS: Array<{ text: string; language: IVRLanguage }> = [
  {
    text: "Welcome to Government Scheme Assistant. For English press 1.",
    language: "english",
  },
  { text: "ಕನ್ನಡಕ್ಕಾಗಿ 2 ಒತ್ತಿರಿ.", language: "kannada" },
  { text: "हिंदी के लिए 3 दबाएं.", language: "hindi" },
  { text: "తెలుగు కోసం 4 నొక్కండి.", language: "telugu" },
  { text: "தமிழுக்கு 5 அழுத்தவும்.", language: "tamil" },
  { text: "Press 6 to exit.", language: "english" },
];

const MENU_TEXT: Record<IVRLanguage, string> = {
  english:
    "Press 1 for Benefits. Press 2 for Eligibility. Press 3 for Documents. Press 4 for Application Process. Press 5 to Repeat Summary. Press 6 to Exit.",
  kannada:
    "ಸೌಲಭ್ಯಗಳಿಗಾಗಿ 1 ಒತ್ತಿರಿ. ಅರ್ಹತೆಯಿಗಾಗಿ 2 ಒತ್ತಿರಿ. ದಾಖಲೆಗಳಿಗಾಗಿ 3 ಒತ್ತಿರಿ. ಅರ್ಜಿಯ ಪ್ರಕ್ರಿಯೆಗೆ 4 ಒತ್ತಿರಿ. ಸಾರಾಂಶವನ್ನು ಮತ್ತೆ ಕೇಳಲು 5 ಒತ್ತಿರಿ. ನಿರ್ಗಮಿಸಲು 6 ಒತ್ತಿರಿ.",
  hindi:
    "लाभों के लिए 1 दबाएं. पात्रता के लिए 2 दबाएं. दस्तावेजों के लिए 3 दबाएं. आवेदन प्रक्रिया के लिए 4 दबाएं. सारांश फिर से सुनने के लिए 5 दबाएं. बाहर निकलने के लिए 6 दबाएं.",
  telugu:
    "లాభాల కోసం 1 నొక్కండి. అర్హత కోసం 2 నొక్కండి. పత్రాల కోసం 3 నొక్కండి. దరఖాస్తు ప్రక్రియ కోసం 4 నొక్కండి. సారాంశాన్ని మళ్లీ వినడానికి 5 నొక్కండి. బయటకు వెళ్లడానికి 6 నొక్కండి.",
  tamil:
    "நன்மைகளுக்கு 1 அழுத்தவும். தகுதிக்கு 2 அழுத்தவும். ஆவணங்களுக்கு 3 அழுத்தவும். விண்ணப்ப செயல்முறைக்கு 4 அழுத்தவும். சுருக்கத்தை மீண்டும் கேட்க 5 அழுத்தவும். வெளியேற 6 அழுத்தவும்.",
};

const SUMMARY_TEXT: Record<IVRLanguage, string> = {
  english:
    "PM Kisan Samman Nidhi Yojana provides financial assistance of ₹6000 per year to eligible farmer families across India. The amount is transferred directly to beneficiaries' bank accounts in three installments.",
  kannada:
    "ಪಿಎಂ ಕಿಸಾನ್ ಸಮ್ಮಾನ್ ನಿಧಿ ಯೋಜನೆಯು ಭಾರತದ ಅರ್ಹ ರೈತ ಕುಟುಂಬಗಳಿಗೆ ವರ್ಷಕ್ಕೆ 6000 ರೂಪಾಯಿ ಆರ್ಥಿಕ ಸಹಾಯವನ್ನು ನೀಡುತ್ತದೆ. ಈ ಮೊತ್ತವನ್ನು ಮೂರು ಕಂತುಗಳಲ್ಲಿ ಫಲಾನುಭವಿಗಳ ಬ್ಯಾಂಕ್ ಖಾತೆಗಳಿಗೆ ನೇರವಾಗಿ ವರ್ಗಾಯಿಸಲಾಗುತ್ತದೆ.",
  hindi:
    "पीएम किसान सम्मान निधि योजना पूरे भारत के पात्र किसान परिवारों को प्रति वर्ष 6000 रुपये की आर्थिक सहायता प्रदान करती है. यह राशि तीन किस्तों में सीधे लाभार्थियों के बैंक खातों में भेजी जाती है.",
  telugu:
    "పీఎం కిసాన్ సమ్మాన్ నిధి యోజన భారతదేశంలోని అర్హులైన రైతు కుటుంబాలకు సంవత్సరానికి 6000 రూపాయల ఆర్థిక సహాయం అందిస్తుంది. ఈ మొత్తం మూడు విడతలుగా లబ్ధిదారుల బ్యాంకు ఖాతాలకు నేరుగా జమ చేయబడుతుంది.",
  tamil:
    "பிஎம் கிசான் சம்மான் நிதி திட்டம் இந்தியா முழுவதும் தகுதியான விவசாய குடும்பங்களுக்கு ஆண்டுக்கு 6000 ரூபாய் நிதி உதவி வழங்குகிறது. இந்த தொகை மூன்று தவணைகளில் பயனாளிகளின் வங்கி கணக்குகளுக்கு நேரடியாக செலுத்தப்படுகிறது.",
};

const SECTION_TEXT: Record<
  "benefits" | "eligibility" | "documents" | "application",
  Record<IVRLanguage, string>
> = {
  benefits: {
    english:
      "Benefits. ₹6000 annual financial support. Direct Benefit Transfer. Available across India. Supports small and marginal farmers.",
    kannada:
      "ಸೌಲಭ್ಯಗಳು. ವರ್ಷಕ್ಕೆ 6000 ರೂಪಾಯಿ ಆರ್ಥಿಕ ಸಹಾಯ. ನೇರ ಲಾಭ ವರ್ಗಾವಣೆ. ಭಾರತದಾದ್ಯಂತ ಲಭ್ಯ. ಸಣ್ಣ ಮತ್ತು ಅತಿ ಸಣ್ಣ ರೈತರಿಗೆ ಬೆಂಬಲ.",
    hindi:
      "लाभ. प्रति वर्ष 6000 रुपये की आर्थिक सहायता. प्रत्यक्ष लाभ अंतरण. पूरे भारत में उपलब्ध. छोटे और सीमांत किसानों को सहायता.",
    telugu:
      "లాభాలు. సంవత్సరానికి 6000 రూపాయల ఆర్థిక సహాయం. ప్రత్యక్ష లాభ బదిలీ. భారతదేశం అంతటా అందుబాటులో ఉంది. చిన్న మరియు సన్నకారు రైతులకు మద్దతు.",
    tamil:
      "நன்மைகள். ஆண்டுக்கு 6000 ரூபாய் நிதி உதவி. நேரடி நன்மை பரிமாற்றம். இந்தியா முழுவதும் கிடைக்கும். சிறு மற்றும் குறு விவசாயிகளுக்கு ஆதரவு.",
  },
  eligibility: {
    english:
      "Eligibility. Applicant must be a farmer. Must own cultivable land. Must be an Indian citizen. Government employees and income tax payers are generally excluded.",
    kannada:
      "ಅರ್ಹತೆ. ಅರ್ಜಿದಾರರು ರೈತರಾಗಿರಬೇಕು. ಕೃಷಿಗೆ ಯೋಗ್ಯವಾದ ಭೂಮಿ ಹೊಂದಿರಬೇಕು. ಭಾರತೀಯ ನಾಗರಿಕರಾಗಿರಬೇಕು. ಸರ್ಕಾರಿ ನೌಕರರು ಮತ್ತು ಆದಾಯ ತೆರಿಗೆ ಪಾವತಿದಾರರನ್ನು ಸಾಮಾನ್ಯವಾಗಿ ಹೊರತುಪಡಿಸಲಾಗುತ್ತದೆ.",
    hindi:
      "पात्रता. आवेदक किसान होना चाहिए. खेती योग्य भूमि होनी चाहिए. भारतीय नागरिक होना चाहिए. सरकारी कर्मचारी और आयकर दाता आमतौर पर शामिल नहीं होते.",
    telugu:
      "అర్హత. దరఖాస్తుదారు రైతు అయి ఉండాలి. సాగుకు అనుకూలమైన భూమి కలిగి ఉండాలి. భారతీయ పౌరుడు అయి ఉండాలి. ప్రభుత్వ ఉద్యోగులు మరియు ఆదాయపు పన్ను చెల్లింపుదారులు సాధారణంగా మినహాయించబడతారు.",
    tamil:
      "தகுதி. விண்ணப்பதாரர் விவசாயியாக இருக்க வேண்டும். பயிரிடக்கூடிய நிலம் இருக்க வேண்டும். இந்திய குடிமகனாக இருக்க வேண்டும். அரசு ஊழியர்கள் மற்றும் வருமான வரி செலுத்துவோர் பொதுவாக விலக்கப்படுவர்.",
  },
  documents: {
    english:
      "Documents. Aadhaar Card. Bank Account Details. Land Ownership Documents. Mobile Number.",
    kannada:
      "ದಾಖಲೆಗಳು. ಆಧಾರ್ ಕಾರ್ಡ್. ಬ್ಯಾಂಕ್ ಖಾತೆ ವಿವರಗಳು. ಭೂ ಮಾಲೀಕತ್ವದ ದಾಖಲೆಗಳು. ಮೊಬೈಲ್ ಸಂಖ್ಯೆ.",
    hindi:
      "दस्तावेज. आधार कार्ड. बैंक खाता विवरण. भूमि स्वामित्व दस्तावेज. मोबाइल नंबर.",
    telugu:
      "పత్రాలు. ఆధార్ కార్డు. బ్యాంకు ఖాతా వివరాలు. భూ యాజమాన్య పత్రాలు. మొబైల్ నంబర్.",
    tamil:
      "ஆவணங்கள். ஆதார் அட்டை. வங்கி கணக்கு விவரங்கள். நில உரிமை ஆவணங்கள். மொபைல் எண்.",
  },
  application: {
    english:
      "Application Process. Visit the PM Kisan portal. Register farmer details. Upload required documents. Submit the application. Verification is done by authorities. Amount is credited after approval.",
    kannada:
      "ಅರ್ಜಿ ಪ್ರಕ್ರಿಯೆ. ಪಿಎಂ ಕಿಸಾನ್ ಪೋರ್ಟಲ್‌ಗೆ ಭೇಟಿ ನೀಡಿ. ರೈತರ ವಿವರಗಳನ್ನು ನೋಂದಾಯಿಸಿ. ಅಗತ್ಯ ದಾಖಲೆಗಳನ್ನು ಅಪ್ಲೋಡ್ ಮಾಡಿ. ಅರ್ಜಿಯನ್ನು ಸಲ್ಲಿಸಿ. ಅಧಿಕಾರಿಗಳು ಪರಿಶೀಲನೆ ಮಾಡುತ್ತಾರೆ. ಅನುಮೋದನೆಯ ನಂತರ ಮೊತ್ತ ಜಮಾ ಆಗುತ್ತದೆ.",
    hindi:
      "आवेदन प्रक्रिया. पीएम किसान पोर्टल पर जाएं. किसान विवरण दर्ज करें. आवश्यक दस्तावेज अपलोड करें. आवेदन जमा करें. अधिकारियों द्वारा सत्यापन किया जाता है. स्वीकृति के बाद राशि जमा होती है.",
    telugu:
      "దరఖాస్తు ప్రక్రియ. పీఎం కిసాన్ పోర్టల్‌ను సందర్శించండి. రైతు వివరాలను నమోదు చేయండి. అవసరమైన పత్రాలను అప్‌లోడ్ చేయండి. దరఖాస్తును సమర్పించండి. అధికారులు ధృవీకరిస్తారు. ఆమోదం తర్వాత మొత్తం జమ అవుతుంది.",
    tamil:
      "விண்ணப்ப செயல்முறை. பிஎம் கிசான் இணையதளத்திற்கு செல்லவும். விவசாயி விவரங்களை பதிவு செய்யவும். தேவையான ஆவணங்களை பதிவேற்றவும். விண்ணப்பத்தை சமர்ப்பிக்கவும். அதிகாரிகள் சரிபார்ப்பார்கள். ஒப்புதல் கிடைத்த பிறகு தொகை வரவு வைக்கப்படும்.",
  },
};

const SUMMARY_SPEECH_FALLBACK: Record<IVRLanguage, string> = {
  english: SUMMARY_TEXT.english,
  kannada:
    "PM Kisan Samman Nidhi Yojane eligible farmer families ge varshake 6000 rupayi financial help koduttade. Ee amount three installments alli beneficiaries bank account ge direct transfer aguttade.",
  hindi:
    "PM Kisan Samman Nidhi Yojana pure Bharat ke patra kisan parivaron ko har saal 6000 rupaye ki arthik sahayata deti hai. Yeh rashi teen kiston mein seedhe labharthiyon ke bank account mein bheji jati hai.",
  telugu:
    "PM Kisan Samman Nidhi Yojana India lo eligible farmer families ki year ki 6000 rupees financial help istundi. Ee amount three installments lo beneficiaries bank accounts ki direct ga transfer avutundi.",
  tamil:
    "PM Kisan Samman Nidhi Yojana India muzhuvathum eligible farmer families ku varudathirku 6000 rupees financial help kodukkirathu. Intha amount three installments la beneficiaries bank account ku direct transfer aagum.",
};

const MENU_SPEECH_FALLBACK: Record<IVRLanguage, string> = {
  english: MENU_TEXT.english,
  kannada:
    "Benefits ge 1 ottiri. Eligibility ge 2 ottiri. Documents ge 3 ottiri. Application process ge 4 ottiri. Summary matte kelalu 5 ottiri. Exit ge 6 ottiri.",
  hindi:
    "Labh ke liye 1 dabayen. Patrata ke liye 2 dabayen. Documents ke liye 3 dabayen. Application process ke liye 4 dabayen. Summary dobara sunne ke liye 5 dabayen. Bahar nikalne ke liye 6 dabayen.",
  telugu:
    "Benefits kosam 1 nokkandi. Eligibility kosam 2 nokkandi. Documents kosam 3 nokkandi. Application process kosam 4 nokkandi. Summary malli vinadaniki 5 nokkandi. Exit kosam 6 nokkandi.",
  tamil:
    "Benefits ku 1 azhuthavum. Eligibility ku 2 azhuthavum. Documents ku 3 azhuthavum. Application process ku 4 azhuthavum. Summary meendum ketka 5 azhuthavum. Exit ku 6 azhuthavum.",
};

const SECTION_SPEECH_FALLBACK: typeof SECTION_TEXT = {
  benefits: {
    english: SECTION_TEXT.benefits.english,
    kannada:
      "Benefits. Varshake 6000 rupayi financial support. Direct Benefit Transfer. India ella kade available. Small and marginal farmers ge support.",
    hindi:
      "Labh. Har saal 6000 rupaye ki arthik sahayata. Direct Benefit Transfer. Pure Bharat mein uplabdh. Chhote aur seemant kisano ko sahayata.",
    telugu:
      "Benefits. Year ki 6000 rupees financial support. Direct Benefit Transfer. India antha available. Small and marginal farmers ki support.",
    tamil:
      "Benefits. Varudathirku 6000 rupees financial support. Direct Benefit Transfer. India muzhuvathum available. Small and marginal farmers ku support.",
  },
  eligibility: {
    english: SECTION_TEXT.eligibility.english,
    kannada:
      "Eligibility. Applicant farmer agirabeku. Cultivable land irabeku. Indian citizen agirabeku. Government employees mattu income tax payers generally excluded.",
    hindi:
      "Patrata. Applicant kisan hona chahiye. Kheti yogya zameen honi chahiye. Bharatiya nagrik hona chahiye. Government employees aur income tax payers aam taur par shamil nahi hote.",
    telugu:
      "Eligibility. Applicant farmer ayi undali. Cultivable land undali. Indian citizen ayi undali. Government employees and income tax payers generally excluded.",
    tamil:
      "Eligibility. Applicant farmer aaga irukka vendum. Cultivable land irukka vendum. Indian citizen aaga irukka vendum. Government employees and income tax payers generally excluded.",
  },
  documents: {
    english: SECTION_TEXT.documents.english,
    kannada:
      "Documents. Aadhaar card. Bank account details. Land ownership documents. Mobile number.",
    hindi:
      "Documents. Aadhaar card. Bank account details. Land ownership documents. Mobile number.",
    telugu:
      "Documents. Aadhaar card. Bank account details. Land ownership documents. Mobile number.",
    tamil:
      "Documents. Aadhaar card. Bank account details. Land ownership documents. Mobile number.",
  },
  application: {
    english: SECTION_TEXT.application.english,
    kannada:
      "Application process. PM Kisan portal ge visit madi. Farmer details register madi. Required documents upload madi. Application submit madi. Authorities verification maduttare. Approval aadmele amount credit aguttade.",
    hindi:
      "Application process. PM Kisan portal par jayen. Farmer details register karen. Required documents upload karen. Application submit karen. Authorities verification karte hain. Approval ke baad amount credit hota hai.",
    telugu:
      "Application process. PM Kisan portal visit cheyandi. Farmer details register cheyandi. Required documents upload cheyandi. Application submit cheyandi. Authorities verification chestaru. Approval tarvata amount credit avutundi.",
    tamil:
      "Application process. PM Kisan portal ku sellavum. Farmer details register seyyavum. Required documents upload seyyavum. Application submit seyyavum. Authorities verification seivargal. Approval pin amount credit aagum.",
  },
};

function findBrowserVoice(langCode: string): SpeechSynthesisVoice | null {
  if (typeof window === "undefined" || !("speechSynthesis" in window)) {
    return null;
  }

  const voices = window.speechSynthesis.getVoices();
  const langPrefix = langCode.split("-")[0];
  return (
    voices.find((voice) => voice.lang === langCode) ||
    voices.find((voice) => voice.lang.toLowerCase().startsWith(langPrefix)) ||
    voices.find((voice) => voice.lang.toLowerCase().startsWith("en")) ||
    null
  );
}

function loadBrowserVoices(): Promise<void> {
  if (typeof window === "undefined" || !("speechSynthesis" in window)) {
    return Promise.resolve();
  }

  if (window.speechSynthesis.getVoices().length > 0) {
    return Promise.resolve();
  }

  return new Promise((resolve) => {
    const timeout = window.setTimeout(resolve, 500);
    window.speechSynthesis.onvoiceschanged = () => {
      window.clearTimeout(timeout);
      resolve();
    };
  });
}

export default function IVRDemoPage() {
  const [callActive, setCallActive] = useState(false);
  const [language, setLanguage] = useState<IVRLanguage | null>(null);
  const [currentSection, setCurrentSection] = useState<CallSection>("greeting");
  const [scheme, setScheme] = useState<IVRScheme | null>(null);
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isMuted, setIsMuted] = useState(false);
  const [volume, setVolume] = useState(80);
  const [elapsedSeconds, setElapsedSeconds] = useState(0);
  const [selectedSection, setSelectedSection] = useState<string | null>(null);
  const [displayText, setDisplayText] = useState<string>("");
  const [isLoading, setIsLoading] = useState(false);
  const playbackResolverRef = useRef<(() => void) | null>(null);
  const sequenceRef = useRef(0);

  // Load scheme data on mount
  useEffect(() => {
    getDemoScheme()
      .then(setScheme)
      .catch((err) => console.error("Error loading scheme:", err));
  }, []);

  // Timer for call duration
  useEffect(() => {
    if (!callActive) return;

    const interval = setInterval(() => {
      setElapsedSeconds((prev) => prev + 1);
    }, 1000);

    return () => clearInterval(interval);
  }, [callActive]);

  // Initial greeting
  useEffect(() => {
    if (callActive && currentSection === "greeting") {
      playGreeting();
    }
  }, [callActive, currentSection]);

  const completePlayback = useCallback(() => {
    const resolve = playbackResolverRef.current;
    playbackResolverRef.current = null;
    setIsPlaying(false);
    if (resolve) resolve();
  }, []);

  const stopPlayback = useCallback(() => {
    window.speechSynthesis?.cancel();
    setAudioBlob(null);
    completePlayback();
  }, [completePlayback]);

  const speakWithBrowser = async (
    text: string,
    lang: IVRLanguage,
    fallbackText?: string,
  ) => {
    if (typeof window === "undefined" || !("speechSynthesis" in window)) {
      console.warn("Speech output is not supported in this browser");
      setIsPlaying(false);
      return;
    }

    await loadBrowserVoices();
    window.speechSynthesis.cancel();

    return new Promise<void>((resolve) => {
      const langCode = SPEECH_LANGUAGE_CODES[lang];
      const voice = findBrowserVoice(langCode);
      const utterance = new SpeechSynthesisUtterance(
        voice ? text : fallbackText || text,
      );
      if (voice) {
        utterance.voice = voice;
        utterance.lang = voice.lang;
      } else {
        utterance.lang = "en-IN";
      }
      utterance.volume = isMuted ? 0 : volume / 100;
      utterance.onend = () => {
        completePlayback();
      };
      utterance.onerror = (event) => {
        if (event.error !== "interrupted" && event.error !== "canceled") {
          console.warn(`Browser speech unavailable: ${event.error}`);
        }
        completePlayback();
      };

      playbackResolverRef.current = resolve;
      setAudioBlob(null);
      setIsPlaying(true);
      window.speechSynthesis.speak(utterance);
    });
  };

  const speakPrompt = async (
    text: string,
    lang: IVRLanguage,
    speechFallbackText?: string,
  ) => {
    setDisplayText(text);

    try {
      const result = await speakText({
        text,
        language: lang,
      });

      if (result.success === false || !result.audio) {
        console.warn(
          `Server speech unavailable, using browser TTS: ${
            result.error || "No audio returned"
          }`,
        );
        await speakWithBrowser(text, lang, speechFallbackText);
        return;
      }

      const blob = audioBase64ToBlob(result.audio);
      await new Promise<void>((resolve) => {
        playbackResolverRef.current = resolve;
        setAudioBlob(blob);
        setIsPlaying(true);
      });
    } catch (error) {
      console.warn(
        `Server speech unavailable, using browser TTS: ${
          error instanceof Error ? error.message : "Speech request failed"
        }`,
      );
      await speakWithBrowser(text, lang, speechFallbackText);
    }
  };

  const playGreeting = async () => {
    setIsLoading(true);
    const sequenceId = ++sequenceRef.current;
    const greetingText = WELCOME_SEGMENTS.map((segment) => segment.text).join(
      " ",
    );

    try {
      setDisplayText(greetingText);
      for (const segment of WELCOME_SEGMENTS) {
        if (sequenceRef.current !== sequenceId || !callActive) return;
        await speakPrompt(segment.text, segment.language);
      }
      setCurrentSection("language");
      setIsLoading(false);
    } catch (err) {
      console.error("Error playing greeting:", err);
      setIsLoading(false);
      setDisplayText(
        `Error: ${err instanceof Error ? err.message : "Failed to play greeting"}`,
      );
    }
  };

  const handleKeyPress = async (key: string) => {
    if (!scheme) return;

    if (currentSection === "greeting" || currentSection === "language") {
      // Language selection
      const languageMap: Record<string, IVRLanguage> = {
        "1": "english",
        "2": "kannada",
        "3": "hindi",
        "4": "telugu",
        "5": "tamil",
        "6": null as any,
      };

      if (key === "6") {
        endCall();
        return;
      }

      const selectedLang = languageMap[key];
      if (selectedLang) {
        sequenceRef.current += 1;
        stopPlayback();
        setLanguage(selectedLang);
        setCurrentSection("summary");
        await playSummary(selectedLang, scheme);
      }
    } else if (currentSection === "menu") {
      // Section selection
      const sectionMap: Record<
        string,
        {
          key:
            | "benefits"
            | "eligibility"
            | "documents"
            | "application"
            | "summary"
            | "exit";
        }
      > = {
        "1": {
          key: "benefits",
        },
        "2": {
          key: "eligibility",
        },
        "3": {
          key: "documents",
        },
        "4": {
          key: "application",
        },
        "5": {
          key: "summary",
        },
        "6": {
          key: "exit",
        },
      };

      const selection = sectionMap[key];
      if (selection) {
        if (selection.key === "exit") {
          endCall();
          return;
        }

        sequenceRef.current += 1;
        stopPlayback();
        setSelectedSection(selection.key);
        if (selection.key === "summary") {
          setCurrentSection("summary");
          await playSummary(language!, scheme);
        } else {
          setCurrentSection("section");
          await playSection(language!, selection.key);
        }
      }
    }
  };

  const playSummary = async (lang: IVRLanguage, _schemeData: IVRScheme) => {
    setIsLoading(true);
    try {
      const textToSpeak = SUMMARY_TEXT[lang];
      await speakPrompt(textToSpeak, lang, SUMMARY_SPEECH_FALLBACK[lang]);
      setCurrentSection("menu");
      await playMenu(lang);
      setIsLoading(false);
    } catch (err) {
      console.error("Error playing summary:", err);
      setIsLoading(false);
    }
  };

  const playMenu = async (lang: IVRLanguage) => {
    setIsLoading(true);
    try {
      const menuText = MENU_TEXT[lang];
      await speakPrompt(menuText, lang, MENU_SPEECH_FALLBACK[lang]);
      setIsLoading(false);
    } catch (err) {
      console.error("Error playing menu:", err);
      setIsLoading(false);
    }
  };

  const playSection = async (
    lang: IVRLanguage,
    sectionKey: "benefits" | "eligibility" | "documents" | "application",
  ) => {
    setIsLoading(true);
    try {
      const textToSpeak = SECTION_TEXT[sectionKey][lang];
      await speakPrompt(
        textToSpeak,
        lang,
        SECTION_SPEECH_FALLBACK[sectionKey][lang],
      );
      setCurrentSection("menu");
      await playMenu(lang);
      setIsLoading(false);
    } catch (err) {
      console.error("Error playing section:", err);
      setIsLoading(false);
    }
  };

  const startCall = () => {
    sequenceRef.current += 1;
    stopPlayback();
    setCallActive(true);
    setLanguage(null);
    setCurrentSection("greeting");
    setElapsedSeconds(0);
    setSelectedSection(null);
    setDisplayText("");
  };

  const endCall = () => {
    sequenceRef.current += 1;
    setCallActive(false);
    setCurrentSection("ended");
    setElapsedSeconds(0);
    stopPlayback();
    setDisplayText("Call Ended");
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900 p-4 md:p-8">
      <div className="max-w-2xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-white mb-2">
            IVR Demo
          </h1>
          <p className="text-gray-400 text-lg">Government Scheme Assistant</p>
        </div>

        {!callActive ? (
          // Initial State - Take a Call Button
          <div className="flex flex-col justify-center items-center min-h-[500px] gap-6">
            {currentSection === "ended" && (
              <p className="text-white text-2xl font-semibold">Call Ended</p>
            )}
            <button
              onClick={startCall}
              disabled={isLoading || !scheme}
              className="
                relative
                group
                px-8 md:px-12 py-6 md:py-8
                bg-gradient-to-r from-green-500 to-emerald-600
                hover:from-green-600 hover:to-emerald-700
                disabled:from-gray-600 disabled:to-gray-700
                text-white font-bold text-2xl md:text-3xl
                rounded-2xl
                transition-all duration-300
                transform hover:scale-105 active:scale-95
                disabled:cursor-not-allowed disabled:opacity-50
                shadow-xl hover:shadow-2xl
                border-2 border-green-400 hover:border-green-300
              "
            >
              <span className="inline-block mr-4 text-4xl group-hover:animate-bounce">
                📞
              </span>
              Take a Call
            </button>
          </div>
        ) : (
          // Active Call State
          <div className="space-y-8">
            {/* Waveform */}
            <div className="flex justify-center">
              <div className="bg-gray-800 rounded-2xl p-8 border border-gray-700">
                <WaveformAnimation isPlaying={isPlaying} />
              </div>
            </div>

            {/* Display Text */}
            <div className="bg-gray-800 border-2 border-gray-700 rounded-2xl p-6 min-h-[120px] flex items-center">
              <p className="text-white text-center text-lg leading-relaxed">
                {displayText || "Listening..."}
              </p>
            </div>

            {/* Call Status Panel */}
            <div className="flex justify-center">
              <CallStatusPanel
                status={
                  isPlaying ? "speaking" : callActive ? "connected" : "ended"
                }
                language={language}
                currentSection={currentSection}
                elapsedSeconds={elapsedSeconds}
                volume={volume}
                onVolumeChange={setVolume}
                onEndCall={endCall}
                isMuted={isMuted}
                onToggleMute={() => setIsMuted(!isMuted)}
              />
            </div>

            {/* Phone Keypad */}
            <div className="flex justify-center">
              <PhoneKeypad onKeyPress={handleKeyPress} enabled={callActive} />
            </div>

            {/* Loading Indicator */}
            {isLoading && (
              <div className="flex justify-center">
                <div className="inline-flex items-center gap-2 bg-blue-900 text-blue-200 px-6 py-3 rounded-full">
                  <div className="w-3 h-3 bg-blue-400 rounded-full animate-pulse" />
                  Processing...
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Hidden Voice Player */}
      <VoicePlayer
        audioBlob={audioBlob}
        isPlaying={isPlaying}
        onPlayComplete={completePlayback}
        onPlaybackError={completePlayback}
        volume={volume}
        isMuted={isMuted}
        autoPlay
      />
    </div>
  );
}
