export default function DashboardShell({ children }: { children: React.ReactNode }) {
  return (
    <main className="min-h-screen bg-gradient-to-br from-orange-50 via-white to-green-50">
      {children}
    </main>
  );
}
