"use client";

import { useEffect, useState } from "react";

export function useVoiceSupport() {
  const [voiceSupported, setVoiceSupported] = useState(false);

  useEffect(() => {
    const speechRecognition =
      (window as any).SpeechRecognition ||
      (window as any).webkitSpeechRecognition;
    setVoiceSupported(Boolean(speechRecognition));
  }, []);

  return voiceSupported;
}
