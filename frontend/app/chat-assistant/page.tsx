"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import SearchBar from "@/components/SearchBar";
import SchemeCard from "@/components/SchemeCard";
import ChatSources from "@/components/home/ChatSources";
import { useAuthSession } from "@/lib/useAuthSession";
import { chatI18n, languageNames } from "@/lib/i18n/chat";
import type { ChatMessage, LanguageCode } from "@/lib/types/chat";
import { streamChat } from "@/lib/api/chat";

export default function ChatAssistantPage() {
  const { token, user, sessionLoading } = useAuthSession();
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [chatLanguage, setChatLanguage] = useState<LanguageCode>("en");
  const [chatLoading, setChatLoading] = useState(false);
  const conversationIdRef = useRef<string>("");
  const messageSeqRef = useRef(0);
  const chatContainerRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    const saved = localStorage.getItem("gs_conversation_id");
    if (saved) {
      conversationIdRef.current = saved;
      return;
    }
    const newId =
      typeof crypto !== "undefined" && "randomUUID" in crypto
        ? (crypto as any).randomUUID()
        : `conv-${Date.now()}-${Math.random().toString(36).slice(2, 10)}`;
    conversationIdRef.current = newId;
    localStorage.setItem("gs_conversation_id", newId);
  }, []);

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop =
        chatContainerRef.current.scrollHeight;
    }
  }, [messages]);

  function nextMessageId(role: "u" | "a") {
    messageSeqRef.current += 1;
    const baseId =
      typeof crypto !== "undefined" && "randomUUID" in crypto
        ? (crypto as any).randomUUID()
        : `${Date.now()}-${Math.random().toString(36).slice(2, 10)}-${messageSeqRef.current}`;
    return `${baseId}-${role}`;
  }

  async function handleChatSearch(q: string) {
    if (!q.trim()) return;

    setChatLoading(true);
    const userMsgId = nextMessageId("u");
    const assistantMsgId = nextMessageId("a");

    const historyForApi = messages
      .filter((m) => m.content.trim() && !m.streaming)
      .slice(-8)
      .map((m) => ({ role: m.role, content: m.content }));

    setMessages((prev) => [
      ...prev,
      { id: userMsgId, role: "user", content: q },
      { id: assistantMsgId, role: "assistant", content: "", streaming: true },
    ]);

    try {
      const queryForBackend =
        chatLanguage !== "en"
          ? `Please answer in ${languageNames[chatLanguage]}. Question: ${q}`
          : q;

      const res = await streamChat({
        query: queryForBackend,
        top_k: 5,
        history: historyForApi,
        conversation_id: conversationIdRef.current,
        language: chatLanguage,
      });

      if (!res.ok) {
        const raw = await res.text();
        setMessages((prev) =>
          prev.map((m) =>
            m.id === assistantMsgId
              ? {
                  ...m,
                  content: raw || "Search failed",
                  streaming: false,
                  error: raw,
                }
              : m,
          ),
        );
        return;
      }

      const reader = res.body!.getReader();
      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n");
        buffer = lines.pop() ?? "";
        for (const line of lines) {
          if (!line.startsWith("data: ")) continue;
          const jsonStr = line.slice(6).trim();
          if (!jsonStr) continue;
          try {
            const event = JSON.parse(jsonStr) as any;
            if (event.type === "token" && event.text) {
              setMessages((prev) =>
                prev.map((m) =>
                  m.id === assistantMsgId
                    ? { ...m, content: m.content + event.text }
                    : m,
                ),
              );
            } else if (event.type === "response_type" && event.value) {
              setMessages((prev) =>
                prev.map((m) =>
                  m.id === assistantMsgId
                    ? { ...m, responseType: event.value }
                    : m,
                ),
              );
            } else if (
              event.type === "scheme" &&
              event.data &&
              !Array.isArray(event.data)
            ) {
              const scheme = event.data;
              setMessages((prev) =>
                prev.map((m) =>
                  m.id === assistantMsgId ? { ...m, scheme } : m,
                ),
              );
            } else if (
              event.type === "relevant_schemes" &&
              Array.isArray(event.data)
            ) {
              const relevantSchemes = event.data;
              setMessages((prev) =>
                prev.map((m) =>
                  m.id === assistantMsgId ? { ...m, relevantSchemes } : m,
                ),
              );
            } else if (event.type === "sources" && Array.isArray(event.data)) {
              setMessages((prev) =>
                prev.map((m) =>
                  m.id === assistantMsgId ? { ...m, sources: event.data } : m,
                ),
              );
            } else if (event.type === "error" && event.text) {
              setMessages((prev) =>
                prev.map((m) =>
                  m.id === assistantMsgId
                    ? { ...m, error: event.text, streaming: false }
                    : m,
                ),
              );
            } else if (event.type === "done") {
              setMessages((prev) =>
                prev.map((m) =>
                  m.id === assistantMsgId ? { ...m, streaming: false } : m,
                ),
              );
            }
          } catch {
            // ignore
          }
        }
      }
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Search failed";
      setMessages((prev) =>
        prev.map((m) =>
          m.id === assistantMsgId
            ? { ...m, content: msg, streaming: false, error: msg }
            : m,
        ),
      );
    } finally {
      setChatLoading(false);
      setMessages((prev) =>
        prev.map((m) =>
          m.id === assistantMsgId ? { ...m, streaming: false } : m,
        ),
      );
    }
  }

  function renderAnswer(text: string) {
    return text.split("\n").map((line, i) => {
      if (!line.trim()) return <div key={i} className="h-2" />;
      const boldMatch = line.match(/^\*\*(.+?)\*\*:??\s*(.*)/);
      if (boldMatch) {
        return (
          <p key={i} className="mt-3 font-bold text-amber-800 text-sm">
            {boldMatch[1]}
            {boldMatch[2] ? ` — ${boldMatch[2]}` : ""}
          </p>
        );
      }
      if (/^[-•*]\s/.test(line)) {
        return (
          <div key={i} className="flex gap-2 mt-1 ml-3">
            <span className="text-amber-500 font-bold mt-0.5">▸</span>
            <span className="text-sm text-gray-800 leading-relaxed">
              {line.replace(/^[-•*]\s/, "")}
            </span>
          </div>
        );
      }
      return (
        <p key={i} className="mt-1 text-sm text-gray-800 leading-relaxed">
          {line}
        </p>
      );
    });
  }

  if (sessionLoading) {
    return (
      <main className="min-h-screen bg-gradient-to-br from-orange-50 via-white to-green-50 flex items-center justify-center p-4">
        <section className="w-full max-w-lg bg-white rounded-2xl border border-orange-100 shadow-xl p-7 text-center">
          <p className="text-sm text-gray-500">Loading session...</p>
        </section>
      </main>
    );
  }

  if (!token) {
    return (
      <main className="min-h-screen bg-gradient-to-br from-orange-50 via-white to-green-50 flex items-center justify-center p-4">
        <section className="w-full max-w-lg bg-white rounded-2xl border border-orange-100 shadow-xl p-7 text-center">
          <h1 className="text-xl font-bold">Chat Assistant</h1>
          <p className="text-sm text-gray-500 mt-2">
            Please login to use the chat assistant.
          </p>
        </section>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-orange-50 via-white to-green-50">
      <section className="max-w-3xl mx-auto px-4 py-8">
        <div className="bg-white rounded-2xl border border-orange-100 shadow-sm p-6">
          <div className="flex items-center justify-between gap-4 mb-4">
            <div>
              <h2 className="text-lg font-bold text-gray-800">
                Government Scheme Assistant
              </h2>
              <p className="text-sm text-gray-500">
                Ask questions and get scheme guidance
              </p>
            </div>
            <div className="flex items-center gap-3">
              <label className="text-sm font-medium text-gray-700">
                Language
              </label>
              <select
                value={chatLanguage}
                onChange={(e) =>
                  setChatLanguage(e.target.value as LanguageCode)
                }
                className="px-3 py-1.5 text-sm border border-gray-300 rounded-lg bg-white"
              >
                {(Object.keys(languageNames) as LanguageCode[]).map((lang) => (
                  <option key={lang} value={lang}>
                    {languageNames[lang]}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div
            ref={chatContainerRef}
            className="mt-3 space-y-4 max-h-[60vh] overflow-y-auto pr-1 scroll-smooth"
          >
            {messages.length === 0 && (
              <p className="text-sm text-gray-400 text-center py-10">
                Start by typing a question
              </p>
            )}
            {messages.map((msg) => (
              <div
                key={msg.id}
                className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
              >
                <div
                  className={`max-w-[85%] ${msg.role === "user" ? "bg-blue-600 text-white rounded-2xl rounded-tr-sm px-4 py-3 text-sm leading-relaxed" : "bg-gray-50 border border-gray-200 rounded-2xl rounded-tl-sm px-4 py-3 w-full"}`}
                >
                  {msg.role === "user" ? (
                    <p>{msg.content}</p>
                  ) : (
                    <>
                      <div className="leading-relaxed">
                        {renderAnswer(msg.content)}
                        {msg.streaming && (
                          <span className="inline-block w-0.5 h-4 bg-amber-600 animate-pulse ml-0.5 align-middle" />
                        )}
                      </div>
                      {msg.error && (
                        <p className="text-red-500 text-xs mt-2">{msg.error}</p>
                      )}
                      <ChatSources sources={msg.sources} />
                      {msg.scheme && (
                        <div className="mt-3">
                          <SchemeCard scheme={msg.scheme} />
                        </div>
                      )}
                      {msg.relevantSchemes &&
                        msg.relevantSchemes.length > 0 && (
                          <div className="mt-3 space-y-3">
                            {msg.relevantSchemes.map((scheme, i) => (
                              <SchemeCard
                                key={`${msg.id}-rel-${i}`}
                                scheme={scheme}
                              />
                            ))}
                          </div>
                        )}
                    </>
                  )}
                </div>
              </div>
            ))}
          </div>

          <div className="mt-4">
            <SearchBar
              value={""}
              onChange={() => {}}
              onSearch={(q) => void handleChatSearch(q)}
              loading={chatLoading}
              placeholder={chatI18n[chatLanguage].search_placeholder}
              buttonText={chatI18n[chatLanguage].search_btn}
              loadingText={chatI18n[chatLanguage].searching}
              ariaLabel={chatI18n[chatLanguage].search_aria}
            />
          </div>
        </div>
      </section>
    </main>
  );
}
