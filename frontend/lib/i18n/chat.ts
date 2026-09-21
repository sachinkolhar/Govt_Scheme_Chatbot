import type { LanguageCode } from "@/lib/types/chat";

export const languageNames: Record<LanguageCode, string> = {
  en: "English",
  hi: "हिन्दी",
  te: "తెలుగు",
  ta: "தமிழ்",
};

export const chatI18n: Record<LanguageCode, Record<string, string>> = {
  en: {
    title: "Ask our AI Assistant",
    subtitle: "Ask me about government schemes, eligibility, benefits & more",
    empty: "No chat history yet. Ask me anything about government schemes!",
    search_placeholder: "e.g. housing scheme, farmer loan, scholarship...",
    search_btn: "Search",
    searching: "Searching...",
    search_aria: "Search government schemes",
    language_label: "Language:",
    awaiting_reply: "Awaiting your yes/no reply",
  },
  hi: {
    title: "हमारे AI सहायक से पूछें",
    subtitle: "सरकारी योजनाओं, पात्रता, लाभ और अन्य जानकारी के बारे में पूछें",
    empty: "अभी कोई चैट इतिहास नहीं है। सरकारी योजनाओं के बारे में पूछें!",
    search_placeholder: "जैसे आवास योजना, किसान ऋण, छात्रवृत्ति...",
    search_btn: "खोजें",
    searching: "खोज रहे हैं...",
    search_aria: "सरकारी योजनाएं खोजें",
    language_label: "भाषा:",
    awaiting_reply: "आपके हां/नहीं उत्तर की प्रतीक्षा है",
  },
  te: {
    title: "మా AI సహాయకుడిని అడగండి",
    subtitle: "ప్రభుత్వ పథకాలు, అర్హత, ప్రయోజనాల గురించి అడగండి",
    empty: "ఇంకా చాట్ చరిత్ర లేదు. ప్రభుత్వ పథకాల గురించి అడగండి!",
    search_placeholder: "ఉదా. హౌసింగ్ పథకం, రైతు రుణం, స్కాలర్‌షిప్...",
    search_btn: "శోధించండి",
    searching: "శోధిస్తున్నాం...",
    search_aria: "ప్రభుత్వ పథకాలను శోధించండి",
    language_label: "భాష:",
    awaiting_reply: "మీ అవును/కాదు సమాధానం కోసం ఎదురు చూస్తున్నాం",
  },
  ta: {
    title: "எங்கள் AI உதவியாளரிடம் கேளுங்கள்",
    subtitle: "அரசு திட்டங்கள், தகுதி, நன்மைகள் பற்றி கேளுங்கள்",
    empty: "இன்னும் சாட் வரலாறு இல்லை. அரசு திட்டங்கள் பற்றி கேளுங்கள்!",
    search_placeholder: "எ.கா. வீட்டுத் திட்டம், விவசாயி கடன், உதவித்தொகை...",
    search_btn: "தேடல்",
    searching: "தேடுகிறது...",
    search_aria: "அரசு திட்டங்களை தேடுங்கள்",
    language_label: "மொழி:",
    awaiting_reply: "உங்கள் ஆம்/இல்லை பதிலுக்காக காத்திருக்கிறது",
  },
};
