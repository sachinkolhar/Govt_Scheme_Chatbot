"use client";

import { useEffect } from "react";

interface PhoneKeypadProps {
  onKeyPress: (key: string) => void;
  enabled: boolean;
}

export default function PhoneKeypad({ onKeyPress, enabled }: PhoneKeypadProps) {
  const keys = [
    ["1", "2", "3"],
    ["4", "5", "6"],
    ["7", "8", "9"],
    ["*", "0", "#"],
  ];

  useEffect(() => {
    if (!enabled) return;

    const handleKeydown = (e: KeyboardEvent) => {
      const key = e.key;
      if (/^[0-9*#]$/.test(key)) {
        e.preventDefault();
        onKeyPress(key);
      }
    };

    window.addEventListener("keydown", handleKeydown);
    return () => window.removeEventListener("keydown", handleKeydown);
  }, [enabled, onKeyPress]);

  const handleClick = (key: string) => {
    if (enabled) {
      onKeyPress(key);
    }
  };

  return (
    <div className="flex justify-center items-center">
      <div className="grid grid-cols-3 gap-2 md:gap-3 bg-gradient-to-b from-gray-800 to-gray-900 p-6 md:p-8 rounded-3xl shadow-2xl border border-gray-700">
        {keys.map((row, rowIdx) => (
          <div key={rowIdx} className="contents">
            {row.map((key) => (
              <button
                key={key}
                onClick={() => handleClick(key)}
                disabled={!enabled}
                className={`
                  w-14 h-14 md:w-16 md:h-16
                  rounded-full
                  font-bold text-lg md:text-xl
                  border-2 border-gray-600
                  transition-all duration-100
                  ${
                    enabled
                      ? "bg-gradient-to-b from-gray-700 to-gray-800 hover:from-blue-600 hover:to-blue-700 text-white hover:text-white cursor-pointer active:scale-95 active:shadow-inner hover:shadow-lg hover:border-blue-500"
                      : "bg-gray-800 text-gray-500 cursor-not-allowed opacity-50"
                  }
                  shadow-md
                `}
              >
                {key}
              </button>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}
