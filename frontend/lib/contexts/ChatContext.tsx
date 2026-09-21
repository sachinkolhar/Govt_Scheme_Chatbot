"use client";

import {
  createContext,
  Dispatch,
  ReactNode,
  SetStateAction,
  useContext,
  useState,
} from "react";
import type { ChatMessage, LanguageCode } from "@/lib/types/chat";

interface ChatContextValue {
  messages: ChatMessage[];
  setMessages: Dispatch<SetStateAction<ChatMessage[]>>;
  language: LanguageCode;
  setLanguage: Dispatch<SetStateAction<LanguageCode>>;
}

const ChatContext = createContext<ChatContextValue | null>(null);

export function ChatProvider({ children }: { children: ReactNode }) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [language, setLanguage] = useState<LanguageCode>("en");

  return (
    <ChatContext.Provider value={{ messages, setMessages, language, setLanguage }}>
      {children}
    </ChatContext.Provider>
  );
}

export function useChatContext() {
  const value = useContext(ChatContext);
  if (!value) {
    throw new Error("useChatContext must be used inside ChatProvider");
  }
  return value;
}
