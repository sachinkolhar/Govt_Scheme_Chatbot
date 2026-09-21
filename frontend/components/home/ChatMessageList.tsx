import type { RefObject } from "react";
import type { ChatMessage } from "@/lib/types/chat";
import ChatMessageBubble from "./ChatMessageBubble";

export default function ChatMessageList({
  messages,
  emptyText,
  containerRef,
}: {
  messages: ChatMessage[];
  emptyText: string;
  containerRef: RefObject<HTMLDivElement>;
}) {
  return (
    <div ref={containerRef} className="mt-5 space-y-4 max-h-[28rem] overflow-y-auto pr-1 scroll-smooth">
      {messages.length === 0 && <p className="text-sm text-gray-400 text-center py-10">{emptyText}</p>}
      {messages.map((message) => <ChatMessageBubble key={message.id} message={message} />)}
    </div>
  );
}
