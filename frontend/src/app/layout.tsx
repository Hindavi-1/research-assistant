import type { Metadata } from "next";
import { Header } from "@/components/layout/Header";
import { Footer } from "@/components/layout/Footer";
import "./globals.css";

export const metadata: Metadata = {
  title: "AI Research Assistant",
  description:
    "Agentic research assistant that discovers literature, identifies gaps, and generates evidence-backed research ideas and titles.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="flex min-h-screen flex-col font-sans">
        <Header />
        <main className="mx-auto w-full max-w-5xl flex-1 px-6 py-8">{children}</main>
        <Footer />
      </body>
    </html>
  );
}
