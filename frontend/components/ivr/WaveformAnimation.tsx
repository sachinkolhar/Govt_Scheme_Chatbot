"use client";

import { useEffect, useState } from "react";

interface WaveformAnimationProps {
  isPlaying: boolean;
}

export default function WaveformAnimation({
  isPlaying,
}: WaveformAnimationProps) {
  const [bars, setBars] = useState<number[]>(Array(12).fill(0));

  useEffect(() => {
    if (!isPlaying) {
      setBars(Array(12).fill(0));
      return;
    }

    const interval = setInterval(() => {
      const newBars = Array(12)
        .fill(0)
        .map(() => Math.random() * 80 + 20);
      setBars(newBars);
    }, 100);

    return () => clearInterval(interval);
  }, [isPlaying]);

  return (
    <div className="flex items-center justify-center gap-1 h-16">
      {bars.map((height, i) => (
        <div
          key={i}
          className={`w-1 rounded-full transition-all duration-100 ${
            isPlaying
              ? "bg-gradient-to-t from-blue-500 to-cyan-400"
              : "bg-gray-500"
          }`}
          style={{
            height: `${height}px`,
          }}
        />
      ))}
    </div>
  );
}
