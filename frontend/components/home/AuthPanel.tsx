import type { FormEvent } from "react";

interface Props {
  mode: "login" | "signup";
  username: string;
  password: string;
  name: string;
  loading: boolean;
  error: string;
  onModeChange: (mode: "login" | "signup") => void;
  onUsernameChange: (value: string) => void;
  onPasswordChange: (value: string) => void;
  onNameChange: (value: string) => void;
  onSubmit: (event: FormEvent) => void;
}

export default function AuthPanel({
  mode,
  username,
  password,
  name,
  loading,
  error,
  onModeChange,
  onUsernameChange,
  onPasswordChange,
  onNameChange,
  onSubmit,
}: Props) {
  return (
    <main className="min-h-screen bg-gradient-to-br from-orange-50 via-white to-green-50 flex items-center justify-center p-4">
      <section className="w-full max-w-lg bg-white rounded-2xl border border-orange-100 shadow-xl p-7">
        <h1 className="text-2xl font-extrabold text-gray-800 text-center">
          Government Scheme Assistant
        </h1>
        <p className="text-sm text-gray-500 text-center mt-2">
          {mode === "login"
            ? "Login to access your personalized dashboard"
            : "Create account and get personalized scheme recommendations"}
        </p>
        <form onSubmit={onSubmit} className="mt-6 space-y-3">
          {mode === "signup" && (
            <input value={name} onChange={(e) => onNameChange(e.target.value)} placeholder="Full name" className="w-full border border-gray-300 rounded-lg px-4 py-2.5" required />
          )}
          <input value={username} onChange={(e) => onUsernameChange(e.target.value)} placeholder="Username" className="w-full border border-gray-300 rounded-lg px-4 py-2.5" required />
          <input value={password} onChange={(e) => onPasswordChange(e.target.value)} placeholder="Password" type="password" className="w-full border border-gray-300 rounded-lg px-4 py-2.5" required />
          {mode === "signup" && <p className="text-xs text-gray-500 leading-relaxed">Password rules: at least 8 characters, 1 uppercase letter, 1 number, and 1 special character.</p>}
          {error && <p className="text-sm text-red-600">{error}</p>}
          <button type="submit" disabled={loading} className="w-full bg-orange-500 hover:bg-orange-600 text-white font-semibold py-2.5 rounded-lg">
            {loading ? "Please wait..." : mode === "login" ? "Login" : "Create Account"}
          </button>
        </form>
        <button type="button" onClick={() => onModeChange(mode === "login" ? "signup" : "login")} className="mt-4 text-sm text-blue-600 hover:underline">
          {mode === "login" ? "New user? Create account" : "Already have an account? Login"}
        </button>
      </section>
    </main>
  );
}
