import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Govt Scheme Chatbot 🇮🇳",
  description:
    "AI-powered Indian Government Scheme Discovery using FAISS semantic search",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
