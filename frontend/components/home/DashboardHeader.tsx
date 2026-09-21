import Link from "next/link";

export default function DashboardHeader({
  greetingName,
  onLogout,
}: {
  greetingName: string;
  onLogout: () => void;
}) {
  return (
    <header className="border-b border-orange-100 bg-white/90 backdrop-blur-sm sticky top-0 z-10">
      <div className="max-w-6xl mx-auto px-4 py-5 flex items-center justify-between gap-3">
        <div>
          <h1 className="text-2xl font-extrabold text-gray-800">
            Government Scheme Assistant
          </h1>
          <p className="text-sm text-gray-500">
            Hello {greetingName} - personalized schemes for your profile
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Link href="/voice" className="text-sm px-4 py-2 rounded-lg border border-blue-300 bg-blue-50 text-blue-700 hover:bg-blue-100">
            Voice
          </Link>
          <button onClick={onLogout} className="text-sm px-4 py-2 rounded-lg border border-gray-300 hover:bg-gray-50">
            Logout
          </button>
        </div>
      </div>
    </header>
  );
}
