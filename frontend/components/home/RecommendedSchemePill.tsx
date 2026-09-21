import type { Scheme } from "@/lib/types/schemes";

const palettes = [
  "border-blue-200 bg-blue-50 text-blue-800",
  "border-emerald-200 bg-emerald-50 text-emerald-800",
  "border-violet-200 bg-violet-50 text-violet-800",
  "border-amber-200 bg-amber-50 text-amber-800",
  "border-rose-200 bg-rose-50 text-rose-800",
  "border-cyan-200 bg-cyan-50 text-cyan-800",
];

export default function RecommendedSchemePill({
  scheme,
  index,
}: {
  scheme: Scheme;
  index: number;
}) {
  return (
    <div className={`rounded-xl border px-4 py-3 ${palettes[index % palettes.length]}`}>
      <p className="text-sm font-semibold">{scheme.scheme_name}</p>
    </div>
  );
}
