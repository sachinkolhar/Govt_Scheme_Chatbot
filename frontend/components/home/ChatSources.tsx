import type { ChatSource } from "@/lib/types/chat";

export default function ChatSources({ sources }: { sources?: ChatSource[] }) {
  const verifiedLinks = (sources ?? []).filter((source) => {
    try { return new URL(source.url).protocol === "https:"; } catch { return false; }
  });
  if (!verifiedLinks.length) return null;
  return (
    <div className="mt-3 border-t border-gray-200 pt-2 text-xs">
      <p className="font-semibold text-gray-600">Official sources</p>
      <ul className="mt-1 space-y-1">
        {verifiedLinks.map((source) => (
          <li key={source.url}>
            <a className="text-blue-700 underline" href={source.url} target="_blank" rel="noopener noreferrer">{source.title}</a>
            {source.retrieved_at && <span className="ml-1 text-gray-500">(retrieved {new Date(source.retrieved_at).toLocaleDateString()})</span>}
          </li>
        ))}
      </ul>
    </div>
  );
}
