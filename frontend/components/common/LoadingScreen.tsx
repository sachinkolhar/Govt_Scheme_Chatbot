export default function LoadingScreen({ text = "Loading session..." }) {
  return (
    <main className="min-h-screen bg-gradient-to-br from-orange-50 via-white to-green-50 flex items-center justify-center p-4">
      <section className="w-full max-w-lg bg-white rounded-2xl border border-orange-100 shadow-xl p-7 text-center">
        <p className="text-sm text-gray-500">{text}</p>
      </section>
    </main>
  );
}
