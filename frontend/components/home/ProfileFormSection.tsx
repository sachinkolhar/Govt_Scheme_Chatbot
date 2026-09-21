import type { FormEvent } from "react";

export default function ProfileFormSection({
  children,
  onSubmit,
}: {
  children: React.ReactNode;
  onSubmit: (event: FormEvent) => void;
}) {
  return (
    <section className="bg-white rounded-2xl border border-orange-100 shadow-sm p-6">
      <h2 className="text-xl font-bold text-gray-800">Find Schemes For Me</h2>
      <p className="text-sm text-gray-500 mt-1">Update your details and run eligibility filtering instantly</p>
      <form onSubmit={onSubmit} className="mt-5 grid md:grid-cols-2 gap-3">
        {children}
      </form>
    </section>
  );
}
