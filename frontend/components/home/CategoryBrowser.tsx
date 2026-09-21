import type { CategorySummary } from "@/lib/types/schemes";

export default function CategoryBrowser({
  categories,
}: {
  categories: CategorySummary[];
}) {
  return (
    <section className="bg-white rounded-2xl border border-orange-100 shadow-sm p-6">
      <h2 className="text-xl font-bold text-gray-800">Browse Schemes</h2>
      <p className="text-sm text-gray-500 mt-1">Explore top scheme categories manually</p>
      <div className="mt-4 flex flex-wrap gap-2">
        {categories.map((item) => (
          <span key={item.category} className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-gray-100 text-gray-700 text-sm">
            {item.category}
            <span className="text-xs text-gray-500">{item.count}</span>
          </span>
        ))}
        {categories.length === 0 && <p className="text-gray-500">No categories available.</p>}
      </div>
    </section>
  );
}
