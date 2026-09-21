import type { Scheme } from "@/lib/types/schemes";
import RecommendedSchemePill from "./RecommendedSchemePill";

export default function RecommendationsSection({
  loading,
  recommendations,
}: {
  loading: boolean;
  recommendations: Scheme[];
}) {
  return (
    <section className="bg-white rounded-2xl border border-orange-100 shadow-sm p-6">
      <h2 className="text-xl font-bold text-gray-800">Recommended Schemes For You</h2>
      <p className="text-sm text-gray-500 mt-1">Based on your saved profile and eligibility conditions</p>
      {loading && <p className="mt-4 text-gray-500">Loading recommendations...</p>}
      {!loading && recommendations.length === 0 && <p className="mt-4 text-gray-500">No recommendations yet. Complete your profile to improve results.</p>}
      {!loading && recommendations.length > 0 && (
        <div className="mt-5 grid gap-3 md:grid-cols-2">
          {recommendations.map((scheme, i) => <RecommendedSchemePill key={`rec-${i}`} scheme={scheme} index={i} />)}
        </div>
      )}
    </section>
  );
}
