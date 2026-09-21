"use client";

import { useEffect, useState } from "react";

interface CallStatusPanelProps {
  status: "ringing" | "connected" | "speaking" | "ended";
  language: string | null;
  currentSection: string;
  elapsedSeconds: number;
  volume: number;
  onVolumeChange: (volume: number) => void;
  onEndCall: () => void;
  isMuted: boolean;
  onToggleMute: () => void;
}

function formatTime(seconds: number): string {
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${mins.toString().padStart(2, "0")}:${secs.toString().padStart(2, "0")}`;
}

export default function CallStatusPanel({
  status,
  language,
  currentSection,
  elapsedSeconds,
  volume,
  onVolumeChange,
  onEndCall,
  isMuted,
  onToggleMute,
}: CallStatusPanelProps) {
  const statusIcons: Record<string, string> = {
    ringing: "📞",
    connected: "🟢",
    speaking: "🔊",
    ended: "🔴",
  };

  const statusLabels: Record<string, string> = {
    ringing: "Ringing...",
    connected: "Connected",
    speaking: "Speaking",
    ended: "Call Ended",
  };

  const sectionLabels: Record<string, string> = {
    greeting: "Greeting",
    language: "Language Selection",
    summary: "Summary",
    menu: "Menu",
    section: "Section",
    ended: "Ended",
  };

  return (
    <div className="bg-gradient-to-b from-gray-900 to-gray-800 border-2 border-gray-700 rounded-2xl p-6 space-y-4 w-full max-w-md">
      {/* Status Row */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <span className="text-2xl">{statusIcons[status]}</span>
          <div>
            <p className="text-xs text-gray-400">Call Status</p>
            <p className="font-bold text-white">{statusLabels[status]}</p>
          </div>
        </div>
        <div className="text-right">
          <p className="text-xs text-gray-400">Duration</p>
          <p className="font-mono font-bold text-green-400">
            {formatTime(elapsedSeconds)}
          </p>
        </div>
      </div>

      <div className="border-t border-gray-700" />

      {/* Language and Section */}
      <div className="grid grid-cols-2 gap-4">
        <div>
          <p className="text-xs text-gray-400 mb-1">Language</p>
          <p className="font-semibold text-white capitalize">
            {language || "Not Selected"}
          </p>
        </div>
        <div>
          <p className="text-xs text-gray-400 mb-1">Section</p>
          <p className="font-semibold text-white capitalize">
            {sectionLabels[currentSection] || currentSection}
          </p>
        </div>
      </div>

      <div className="border-t border-gray-700" />

      {/* Volume Control */}
      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <label className="text-sm font-semibold text-gray-300">Volume</label>
          <span className="text-sm font-bold text-blue-400">
            {Math.round(volume)}%
          </span>
        </div>
        <input
          type="range"
          min="0"
          max="100"
          value={volume}
          onChange={(e) => onVolumeChange(Number(e.target.value))}
          className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-blue-500"
        />
      </div>

      {/* Mute and End Call Buttons */}
      <div className="flex gap-3 pt-2">
        <button
          onClick={onToggleMute}
          className={`flex-1 py-2 px-4 rounded-lg font-semibold transition-all ${
            isMuted
              ? "bg-red-600 text-white hover:bg-red-700"
              : "bg-gray-700 text-white hover:bg-gray-600"
          }`}
        >
          {isMuted ? "🔇 Muted" : "🔊 Mute"}
        </button>
        <button
          onClick={onEndCall}
          className="flex-1 py-2 px-4 rounded-lg font-semibold bg-red-600 text-white hover:bg-red-700 transition-all"
        >
          ☎️ End Call
        </button>
      </div>
    </div>
  );
}
