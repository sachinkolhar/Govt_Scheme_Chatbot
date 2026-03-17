"use client";

import { KeyboardEvent } from "react";

interface Props {
  value: string;
  onChange: (value: string) => void;
  onSearch: (value: string) => void;
  loading: boolean;
  placeholder?: string;
  buttonText?: string;
  loadingText?: string;
  ariaLabel?: string;
}

export default function SearchBar({
  value,
  onChange,
  onSearch,
  loading,
  placeholder = "e.g. housing scheme for poor families, farmer loan waiver, scholarship for students…",
  buttonText = "Search",
  loadingText = "Searching…",
  ariaLabel = "Search government schemes",
}: Props) {
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch(value);
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") onSearch(value);
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-3">
      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder={placeholder}
        className="flex-1 border border-gray-300 rounded-xl px-5 py-3 text-gray-800 placeholder-gray-400
                   focus:outline-none focus:ring-2 focus:ring-orange-400 shadow-sm text-base"
        disabled={loading}
        aria-label={ariaLabel}
      />
      <button
        type="submit"
        disabled={loading || !value.trim()}
        className="bg-orange-500 hover:bg-orange-600 disabled:bg-orange-300 text-white font-semibold
                   px-7 py-3 rounded-xl shadow-sm transition-colors whitespace-nowrap cursor-pointer"
      >
        {loading ? (
          <span className="flex items-center gap-2">
            <span className="animate-spin inline-block w-4 h-4 border-2 border-white border-t-transparent rounded-full" />
            {loadingText}
          </span>
        ) : (
          buttonText
        )}
      </button>
    </form>
  );
}
