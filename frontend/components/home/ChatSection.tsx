export default function ChatSection({ children }: { children: React.ReactNode }) {
  return (
    <section className="bg-white rounded-2xl border border-orange-100 shadow-sm p-6">
      {children}
    </section>
  );
}
