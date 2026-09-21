"use client";

import { useRef, useState } from "react";
import * as audioApi from "@/lib/audioApi";

interface MicButtonProps {
  language: string;
  onTranscript: (transcript: string) => void;
  onError: (error: string) => void;
  onBeforeStart?: () => void | Promise<void>;
  disabled?: boolean;
  isInFlow?: boolean;
}

export default function MicButton({
  language,
  onTranscript,
  onError,
  onBeforeStart,
  disabled = false,
}: MicButtonProps) {
  const [isListening, setIsListening] = useState(false);
  const [isPreparing, setIsPreparing] = useState(false);
  const [transcript, setTranscript] = useState("");
  const isRecordingRef = useRef(false);
  const stopRecordingRef = useRef<AbortController | null>(null);

  const startListening = async () => {
    setTranscript("");
    onError("");
    setIsPreparing(true);

    try {
      await onBeforeStart?.();

      const stopController = new AbortController();
      stopRecordingRef.current = stopController;
      setIsListening(true);
      isRecordingRef.current = true;

      if (audioApi.isBrowserSpeechRecognitionSupported()) {
        const browserTranscript = await audioApi.recognizeSpeechWithBrowser(
          language,
          setTranscript,
          onError,
          30000,
          stopController.signal,
        );

        if (browserTranscript && isRecordingRef.current) {
          setTranscript(browserTranscript);
          onTranscript(browserTranscript);
        }
        return;
      }

      // Start recording with MediaRecorder
      const audioBlob = await audioApi.recordAudioWithMediaRecorder(
        (text) => {
          setTranscript(text);
        },
        (error) => {
          onError(error);
          setIsListening(false);
        },
        30000,
        stopController.signal,
      );

      if (!audioBlob || !isRecordingRef.current) {
        setIsListening(false);
        return;
      }

      // Send audio to backend for transcription
      setTranscript("Processing audio...");
      const response = await audioApi.transcribeAudio(audioBlob, language);

      if (response.success && response.data) {
        setTranscript(response.data);
        onTranscript(response.data);
      } else {
        const errorMsg =
          response.error ||
          "Transcription failed. Please try again with clearer speech.";
        onError(errorMsg);
        setTranscript("");
      }
    } catch (error) {
      const message =
        error instanceof Error ? error.message : "Recording failed";
      onError(message);
      setTranscript("");
    } finally {
      setIsListening(false);
      setIsPreparing(false);
      isRecordingRef.current = false;
      stopRecordingRef.current = null;
    }
  };

  const stopListening = () => {
    stopRecordingRef.current?.abort();
    setIsListening(false);
  };

  return (
    <div className="flex flex-col gap-2">
      <button
        type="button"
        onClick={isListening ? stopListening : startListening}
        disabled={disabled || isPreparing}
        className={`px-6 py-3 rounded-lg font-semibold transition-colors flex items-center justify-center gap-2 ${
          isListening
            ? "bg-red-500 hover:bg-red-600 text-white"
            : "bg-blue-500 hover:bg-blue-600 disabled:bg-gray-300 text-white"
        }`}
        title={isListening ? "Stop recording" : "Click to speak"}
      >
        {isPreparing ? (
          <>Preparing...</>
        ) : isListening ? (
          <>
            <span className="animate-pulse inline-block w-3 h-3 bg-white rounded-full"></span>
            Stop Recording
          </>
        ) : (
          <>
            <span>🎤</span>
            Start Listening
          </>
        )}
      </button>

      {/* Live transcript preview */}
      {isListening && transcript && (
        <div className="text-sm bg-blue-50 border border-blue-200 rounded-lg px-3 py-2 text-blue-900">
          <span className="font-semibold">
            {transcript === "Recording... speak now"
              ? "Recording: "
              : "Processing: "}
          </span>
          {transcript}
        </div>
      )}
    </div>
  );
}
