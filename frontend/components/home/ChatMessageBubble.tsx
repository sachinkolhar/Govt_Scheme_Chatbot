import SchemeCard from "@/components/SchemeCard";
import type { ChatMessage } from "@/lib/types/chat";
import AnswerText from "./AnswerText";

export default function ChatMessageBubble({ message }: { message: ChatMessage }) {
  return (
    <div className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}>
      <div className={`max-w-[85%] ${message.role === "user" ? "bg-blue-600 text-white rounded-2xl rounded-tr-sm px-4 py-3 text-sm leading-relaxed" : "bg-gray-50 border border-gray-200 rounded-2xl rounded-tl-sm px-4 py-3 w-full"}`}>
        {message.role === "user" ? (
          <p>{message.content}</p>
        ) : (
          <>
            <div className="leading-relaxed">
              <AnswerText text={message.content} />
              {message.streaming && <span className="inline-block w-0.5 h-4 bg-amber-600 animate-pulse ml-0.5 align-middle" />}
            </div>
            {message.error && <p className="text-red-500 text-xs mt-2">{message.error}</p>}
            {message.sources && message.sources.length > 0 && (
              <div className="mt-3 border-t border-gray-200 pt-2 text-xs">
                <p className="font-semibold text-gray-600">Official sources</p>
                <ul className="mt-1 space-y-1">
                  {message.sources.map((source) => {
                    let isHttps = false;
                    try { isHttps = new URL(source.url).protocol === "https:"; } catch { /* Invalid source URLs are not linked. */ }
                    return <li key={source.url}>{isHttps ? <a className="text-blue-700 underline" href={source.url} target="_blank" rel="noopener noreferrer">{source.title}</a> : <span>{source.title} (link unavailable)</span>}</li>;
                  })}
                </ul>
              </div>
            )}
            {message.scheme && <div className="mt-3"><SchemeCard scheme={message.scheme} /></div>}
            {message.relevantSchemes && message.relevantSchemes.length > 0 && (
              <div className="mt-3 space-y-3">
                {message.relevantSchemes.map((scheme, i) => <SchemeCard key={`${message.id}-rel-${i}`} scheme={scheme} />)}
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
