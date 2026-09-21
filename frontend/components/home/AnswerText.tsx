export default function AnswerText({ text }: { text: string }) {
  return (
    <>
      {text.split("\n").map((line, i) => {
        if (!line.trim()) return <div key={i} className="h-2" />;
        const boldMatch = line.match(/^\*\*(.+?)\*\*:?\s*(.*)/);
        if (boldMatch) {
          return (
            <p key={i} className="mt-3 font-bold text-amber-800 text-sm">
              {boldMatch[1]}
              {boldMatch[2] ? ` - ${boldMatch[2]}` : ""}
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
      })}
    </>
  );
}
