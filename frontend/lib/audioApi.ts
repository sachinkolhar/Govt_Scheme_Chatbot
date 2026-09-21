/**
 * Frontend API client for speech-to-text and text-to-speech operations.
 * Communicates with backend /api/audio/* endpoints.
 */

export interface SpeechRequest {
  audio_base64?: string;
  text?: string;
  language: string;
  format?: string;
}

export interface SpeechResponse {
  success: boolean;
  data?: string; // Transcribed text (STT) or base64 audio (TTS)
  error?: string;
  language: string;
}

function browserLangCode(language: string): string {
  const normalized = (language || "en").toLowerCase();
  const map: Record<string, string> = {
    en: "en-US",
    hi: "hi-IN",
    te: "te-IN",
    ta: "ta-IN",
  };
  return map[normalized] || "en-US";
}

function browserSpeechRecognitionConstructor(): any {
  if (typeof window === "undefined") return null;
  return (
    (window as any).SpeechRecognition ||
    (window as any).webkitSpeechRecognition ||
    (window as any).mozSpeechRecognition ||
    null
  );
}

export function isBrowserSpeechRecognitionSupported(): boolean {
  return Boolean(browserSpeechRecognitionConstructor());
}

export function isMediaRecorderSupported(): boolean {
  return Boolean(
    typeof window !== "undefined" &&
    typeof MediaRecorder !== "undefined" &&
    navigator.mediaDevices?.getUserMedia,
  );
}

async function speakWithBrowserTTS(
  text: string,
  language: string,
): Promise<{ success: boolean; error?: string }> {
  if (typeof window === "undefined" || !("speechSynthesis" in window)) {
    return {
      success: false,
      error: "Speech output is not supported in this browser",
    };
  }

  return new Promise((resolve) => {
    try {
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = browserLangCode(language);
      utterance.onend = () => resolve({ success: true });
      utterance.onerror = () =>
        resolve({ success: false, error: "Browser speech playback failed" });
      window.speechSynthesis.cancel();
      window.speechSynthesis.speak(utterance);
    } catch (error) {
      const errorMsg =
        error instanceof Error
          ? error.message
          : "Browser speech playback failed";
      resolve({ success: false, error: errorMsg });
    }
  });
}

export async function recognizeSpeechWithBrowser(
  language: string,
  onTranscript: (transcript: string) => void,
  onError: (error: string) => void,
  maxDuration: number = 30000,
  stopSignal?: AbortSignal,
): Promise<string | null> {
  const SpeechRecognition = browserSpeechRecognitionConstructor();
  if (!SpeechRecognition) return null;

  return new Promise((resolve) => {
    const recognition = new SpeechRecognition();
    recognition.lang = browserLangCode(language);
    recognition.interimResults = true;
    recognition.continuous = true;
    recognition.maxAlternatives = 1;

    let finalTranscript = "";
    let latestTranscript = "";
    let settled = false;
    let timeoutId: NodeJS.Timeout | null = null;

    const cleanup = () => {
      if (timeoutId) clearTimeout(timeoutId);
      stopSignal?.removeEventListener("abort", stopRecognition);
    };

    const finish = () => {
      if (settled) return;
      settled = true;
      cleanup();
      resolve((finalTranscript || latestTranscript).trim() || null);
    };

    function stopRecognition() {
      try {
        recognition.stop();
      } catch {
        finish();
      }
    }

    recognition.onstart = () => {
      onTranscript("Listening... speak now");
      timeoutId = setTimeout(stopRecognition, maxDuration);
    };

    recognition.onresult = (event: any) => {
      let interimTranscript = "";
      for (let i = event.resultIndex; i < event.results.length; i++) {
        const transcript = event.results[i][0].transcript;
        if (event.results[i].isFinal) {
          finalTranscript += `${transcript} `;
        } else {
          interimTranscript += transcript;
        }
      }
      latestTranscript = (finalTranscript + interimTranscript).trim();
      if (latestTranscript) onTranscript(latestTranscript);
    };

    recognition.onerror = (event: any) => {
      const errorCode = event.error;
      if (errorCode === "no-speech") {
        onError("No speech detected. Please speak louder or try again.");
      } else if (errorCode === "audio-capture") {
        onError("Could not access microphone. Please check permissions.");
      } else if (errorCode === "not-allowed") {
        onError(
          "Microphone permission denied. Please allow microphone access.",
        );
      } else {
        onError(`Speech error: ${errorCode}`);
      }
    };

    recognition.onend = finish;

    try {
      stopSignal?.addEventListener("abort", stopRecognition, { once: true });
      recognition.start();
    } catch (error) {
      cleanup();
      const errorMsg =
        error instanceof Error ? error.message : "Failed to start speech";
      onError(errorMsg);
      resolve(null);
    }
  });
}

/**
 * Convert Blob audio to base64 string.
 */
export async function blobToBase64(blob: Blob): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onloadend = () => {
      const result = reader.result as string;
      // Remove the "data:audio/...;base64," prefix
      const base64 = result.split(",")[1];
      resolve(base64);
    };
    reader.onerror = reject;
    reader.readAsDataURL(blob);
  });
}

function audioFormatFromBlob(blob: Blob): string {
  const mimeType = blob.type.toLowerCase();
  if (mimeType.includes("webm")) return "webm";
  if (mimeType.includes("ogg")) return "ogg";
  if (mimeType.includes("mpeg") || mimeType.includes("mp3")) return "mp3";
  if (mimeType.includes("mp4") || mimeType.includes("m4a")) return "m4a";
  if (mimeType.includes("wav")) return "wav";
  return "webm";
}

/**
 * Convert base64 audio string to Blob.
 */
export function base64ToBlob(
  base64: string,
  mimeType: string = "audio/mpeg",
): Blob {
  try {
    if (!base64 || typeof base64 !== "string") {
      throw new Error("Invalid base64 string provided");
    }

    // Clean up base64 string - remove whitespace and data URI prefix if present
    let cleanedBase64 = base64.trim();
    if (cleanedBase64.startsWith("data:")) {
      const parts = cleanedBase64.split(",");
      if (parts.length > 1) {
        cleanedBase64 = parts[1];
      }
    }

    // Decode base64 to binary string
    const binaryString = atob(cleanedBase64);
    const bytes = new Uint8Array(binaryString.length);
    for (let i = 0; i < binaryString.length; i++) {
      bytes[i] = binaryString.charCodeAt(i);
    }

    const blob = new Blob([bytes], { type: mimeType });
    console.log(
      `Created audio blob: ${blob.size} bytes, MIME type: ${mimeType}`,
    );
    return blob;
  } catch (error) {
    console.error("Error converting base64 to blob:", error);
    throw error;
  }
}

function isLikelyPlayableMp3(blob: Blob): Promise<boolean> {
  return blob
    .slice(0, 16)
    .arrayBuffer()
    .then((buffer) => {
      const bytes = new Uint8Array(buffer);
      if (bytes.length < 4 || blob.size < 128) return false;

      const hasId3Header =
        bytes[0] === 0x49 && bytes[1] === 0x44 && bytes[2] === 0x33;
      const hasFrameSync =
        bytes[0] === 0xff && (bytes[1] & 0xe0) === 0xe0;

      return hasId3Header || hasFrameSync;
    });
}

/**
 * Send audio blob to backend for transcription.
 */
export async function transcribeAudio(
  audioBlob: Blob,
  language: string = "en",
): Promise<SpeechResponse> {
  try {
    const audio_base64 = await blobToBase64(audioBlob);
    const format = audioFormatFromBlob(audioBlob);

    const response = await fetch("/api/audio/transcribe", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        audio_base64,
        language,
        format,
      } as SpeechRequest),
    });

    if (!response.ok) {
      throw new Error(`Transcription failed: ${response.statusText}`);
    }

    return (await response.json()) as SpeechResponse;
  } catch (error) {
    const errorMsg = error instanceof Error ? error.message : "Unknown error";
    return {
      success: false,
      error: errorMsg,
      language,
    };
  }
}

/**
 * Send text to backend for synthesis and play the audio.
 */
export async function synthesizeAndPlayAudio(
  text: string,
  language: string = "en",
): Promise<{ success: boolean; error?: string }> {
  const fallbackToBrowserTTS = async () => {
    return speakWithBrowserTTS(text, language);
  };

  try {
    if (!text.trim()) {
      return { success: false, error: "No text to synthesize" };
    }

    const response = await fetch("/api/audio/synthesize", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        text,
        language,
      } as SpeechRequest),
    });

    if (!response.ok) {
      console.warn(`Synthesis request failed with status ${response.status}`);
      return fallbackToBrowserTTS();
    }

    const result = (await response.json()) as SpeechResponse;

    if (!result.success || !result.data) {
      console.warn(`Synthesis failed: ${result.error || "Unknown error"}`);
      return fallbackToBrowserTTS();
    }

    console.log(
      `Audio synthesis successful: ${result.data.length} characters in base64`,
    );

    try {
      // Convert base64 to Blob and play
      const audioBlob = base64ToBlob(result.data, "audio/mpeg");
      console.log(
        `Converted to blob: ${audioBlob.size} bytes, MIME: ${audioBlob.type}`,
      );
      if (!(await isLikelyPlayableMp3(audioBlob))) {
        throw new Error("Backend returned invalid or incomplete MP3 audio");
      }
      await playAudioBlob(audioBlob);
      return { success: true };
    } catch (playError) {
      const errorMsg =
        playError instanceof Error ? playError.message : String(playError);
      console.error("Audio playback error:", errorMsg);
      // Fall back to browser TTS if server audio playback fails
      return fallbackToBrowserTTS();
    }
  } catch (error) {
    const errorMsg = error instanceof Error ? error.message : String(error);
    console.error("Synthesis error:", errorMsg);
    return fallbackToBrowserTTS();
  }
}

/**
 * Play an audio blob in the browser.
 * Returns a promise that resolves when playback starts or rejects on error.
 */
export async function playAudioBlob(blob: Blob): Promise<void> {
  return new Promise((resolve, reject) => {
    try {
      // Validate blob
      if (!blob || blob.size === 0) {
        reject(new Error("Audio blob is empty or invalid"));
        return;
      }

      console.log(`Playing audio blob: ${blob.size} bytes, type: ${blob.type}`);

      const url = URL.createObjectURL(blob);
      const audio = new Audio(url);

      // Set a timeout in case playback hangs
      const timeoutId = setTimeout(() => {
        URL.revokeObjectURL(url);
        reject(new Error("Audio playback timeout - no data received"));
      }, 5000);

      // Handle playback ended
      audio.onended = () => {
        clearTimeout(timeoutId);
        URL.revokeObjectURL(url);
        resolve();
      };

      // Handle errors during playback
      audio.onerror = () => {
        clearTimeout(timeoutId);
        URL.revokeObjectURL(url);
        const errorCode = audio.error?.code;
        const errorMap: Record<number, string> = {
          1: "MEDIA_ERR_ABORTED",
          2: "MEDIA_ERR_NETWORK",
          3: "MEDIA_ERR_DECODE",
          4: "MEDIA_ERR_SRC_NOT_SUPPORTED",
        };
        const errorName = errorMap[errorCode || 0] || "UNKNOWN_ERROR";
        const errorMessage = audio.error?.message || "Unknown audio error";
        console.error(
          `Audio error ${errorCode} (${errorName}): ${errorMessage}`,
        );
        reject(
          new Error(
            `Audio playback error: ${errorName} - Audio format may not be supported`,
          ),
        );
      };

      // Handle abort
      audio.onabort = () => {
        clearTimeout(timeoutId);
        URL.revokeObjectURL(url);
        reject(new Error("Audio playback aborted"));
      };

      // Start playing - returns a promise in modern browsers
      const playPromise = audio.play();
      if (playPromise !== undefined) {
        playPromise
          .then(() => {
            console.log("Audio playback started successfully");
            clearTimeout(timeoutId);
          })
          .catch((err) => {
            clearTimeout(timeoutId);
            URL.revokeObjectURL(url);
            reject(
              new Error(
                `Failed to start audio playback: ${err instanceof Error ? err.message : String(err)}`,
              ),
            );
          });
      }
    } catch (error) {
      reject(error instanceof Error ? error : new Error(String(error)));
    }
  });
}

/**
 * Record audio using MediaRecorder API with enhanced audio quality.
 * Better accuracy than Web Speech API, works with Whisper backend.
 */
export async function recordAudioWithMediaRecorder(
  onTranscript: (transcript: string) => void,
  onError: (error: string) => void,
  maxDuration: number = 30000, // 30 seconds max
  stopSignal?: AbortSignal,
): Promise<Blob | null> {
  try {
    // Request microphone with audio enhancements for better quality
    const stream = await navigator.mediaDevices.getUserMedia({
      audio: {
        echoCancellation: true, // Remove background echo
        noiseSuppression: true, // Filter background noise
        autoGainControl: true, // Normalize loud/quiet speech
        sampleRate: 16000, // Optimal for Whisper
        channelCount: 1, // Mono is enough for speech
      },
    });

    // Determine supported MIME type
    const mimeType = MediaRecorder.isTypeSupported("audio/webm;codecs=opus")
      ? "audio/webm;codecs=opus"
      : MediaRecorder.isTypeSupported("audio/mp3")
        ? "audio/mp3"
        : "audio/wav";

    const mediaRecorder = new MediaRecorder(stream, { mimeType });
    const audioChunks: BlobPart[] = [];

    mediaRecorder.ondataavailable = (event) => {
      if (event.data.size > 0) {
        audioChunks.push(event.data);
      }
    };

    return new Promise((resolve, reject) => {
      let timeoutId: NodeJS.Timeout | null = null;
      let settled = false;

      const cleanup = () => {
        if (timeoutId) clearTimeout(timeoutId);
        stopSignal?.removeEventListener("abort", stopRecording);
        stream.getTracks().forEach((track) => track.stop());
      };

      const finish = (audioBlob: Blob | null) => {
        if (settled) return;
        settled = true;
        cleanup();
        resolve(audioBlob);
      };

      function stopRecording() {
        if (mediaRecorder.state === "recording") {
          mediaRecorder.stop();
        } else {
          finish(null);
        }
      }

      mediaRecorder.onstop = () => {
        if (audioChunks.length === 0) {
          finish(null);
          return;
        }
        finish(new Blob(audioChunks, { type: mimeType }));
      };

      mediaRecorder.onerror = (error) => {
        if (settled) return;
        settled = true;
        cleanup();
        const errorMsg =
          error instanceof Error ? error.message : "Recording error occurred";
        onError(errorMsg);
        reject(new Error(errorMsg));
      };

      // Auto-stop after max duration
      timeoutId = setTimeout(() => {
        if (mediaRecorder.state === "recording") {
          mediaRecorder.stop();
        }
      }, maxDuration);

      try {
        stopSignal?.addEventListener("abort", stopRecording, { once: true });
        mediaRecorder.start();
        onTranscript("Recording... speak now");
      } catch (error) {
        settled = true;
        cleanup();
        const errorMsg =
          error instanceof Error ? error.message : "Failed to start recording";
        onError(errorMsg);
        reject(new Error(errorMsg));
      }
    });
  } catch (error) {
    let errorMsg = "Microphone access denied";
    if (error instanceof DOMException) {
      if (error.name === "NotAllowedError") {
        errorMsg =
          "Microphone permission denied. Please allow access in browser settings.";
      } else if (error.name === "NotFoundError") {
        errorMsg = "No microphone found. Please check your audio device.";
      }
    }
    onError(errorMsg);
    return null;
  }
}

/**
 * Setup browser Web Speech API for speech recognition.
 */
export function initializeSpeechRecognition(
  language: string,
  onTranscript: (transcript: string) => void,
  onError: (error: string) => void,
  onEnd: () => void,
): any {
  // Use browser's Web Speech API (with vendor prefixes for cross-browser support)
  const SpeechRecognition =
    (window as any).SpeechRecognition ||
    (window as any).webkitSpeechRecognition ||
    (window as any).mozSpeechRecognition;

  if (!SpeechRecognition) {
    onError("Speech Recognition not supported in this browser");
    return null;
  }

  const recognition = new SpeechRecognition();
  const langMap: Record<string, string> = {
    en: "en-US",
    hi: "hi-IN",
    te: "te-IN",
    ta: "ta-IN",
  };

  recognition.language = langMap[language] || "en-US";
  recognition.interimResults = true; // Enable live transcript preview
  recognition.continuous = true; // Keep listening through pauses
  recognition.maxAlternatives = 1; // Single best match

  let finalTranscript = "";
  let latestTranscript = "";
  let silenceTimeout: NodeJS.Timeout | null = null;
  let speechDetected = false;

  recognition.onstart = () => {
    finalTranscript = "";
    latestTranscript = "";
    speechDetected = false;
    onTranscript("");
    // Auto-stop if no speech detected within 5 seconds
    silenceTimeout = setTimeout(() => {
      if (!speechDetected && recognition) {
        recognition.stop();
      }
    }, 5000);
  };

  recognition.onresult = (event: any) => {
    if (silenceTimeout) {
      clearTimeout(silenceTimeout);
      silenceTimeout = null;
    }
    speechDetected = true;
    let interimTranscript = "";
    for (let i = event.resultIndex; i < event.results.length; i++) {
      const transcript = event.results[i][0].transcript;
      if (event.results[i].isFinal) {
        finalTranscript += transcript + " ";
      } else {
        interimTranscript += transcript;
      }
    }
    // Show live preview of transcript
    latestTranscript = (finalTranscript + interimTranscript).trim();
    onTranscript(latestTranscript);
  };

  recognition.onerror = (event: any) => {
    const errorCode = event.error;
    let errorMessage = `Speech error: ${errorCode}`;

    // Provide more helpful error messages
    if (errorCode === "no-speech") {
      errorMessage = "No speech detected. Please speak louder or try again.";
    } else if (errorCode === "audio-capture") {
      errorMessage = "Could not access microphone. Please check permissions.";
    } else if (errorCode === "network") {
      errorMessage = "Network error. Please try again.";
    }

    onError(errorMessage);
  };

  recognition.onend = () => {
    if (silenceTimeout) {
      clearTimeout(silenceTimeout);
    }
    onTranscript((finalTranscript || latestTranscript).trim());
    onEnd();
  };

  return recognition;
}
