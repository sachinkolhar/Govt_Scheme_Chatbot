"use client";

import { useEffect, useRef, useState } from "react";

interface VoicePlayerProps {
  audioBlob: Blob | null;
  isPlaying: boolean;
  onPlayComplete: () => void;
  onPlaybackError?: () => void;
  volume: number;
  isMuted: boolean;
  autoPlay?: boolean;
}

export default function VoicePlayer({
  audioBlob,
  isPlaying,
  onPlayComplete,
  onPlaybackError,
  volume,
  isMuted,
  autoPlay = true,
}: VoicePlayerProps) {
  const audioRef = useRef<HTMLAudioElement>(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const audio = audioRef.current;
    if (!audio) return;

    if (!audioBlob) {
      audio.pause();
      audio.removeAttribute("src");
      audio.load();
      setIsLoading(false);
      return;
    }

    const url = URL.createObjectURL(audioBlob);
    audio.src = url;
    audio.load();

    return () => {
      audio.pause();
      audio.removeAttribute("src");
      audio.load();
      URL.revokeObjectURL(url);
    };
  }, [audioBlob]);

  useEffect(() => {
    const audio = audioRef.current;
    if (!audio || !audioBlob) return;

    if (isPlaying && autoPlay) {
      setIsLoading(true);
      audio.play().catch((err) => {
        if (err instanceof DOMException && err.name === "AbortError") return;
        console.warn("Audio playback unavailable:", err);
        onPlaybackError?.();
      });
    } else {
      audio.pause();
      setIsLoading(false);
    }
  }, [audioBlob, isPlaying, autoPlay, onPlaybackError]);

  useEffect(() => {
    if (!audioRef.current) return;
    audioRef.current.volume = isMuted ? 0 : volume / 100;
  }, [volume, isMuted]);

  const handleEnded = () => {
    setIsLoading(false);
    onPlayComplete();
  };

  const handleLoadStart = () => {
    setIsLoading(true);
  };

  return (
    <audio
      ref={audioRef}
      onEnded={handleEnded}
      onLoadStart={handleLoadStart}
      onCanPlay={() => setIsLoading(false)}
      className="hidden"
    />
  );
}
