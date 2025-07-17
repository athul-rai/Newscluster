"use client";

import ClusteredNews from "@/components/ClusteredNews";
import Navbar from "@/components/Navbar";

export default function Home() {
  return (
    <div className="grid grid-rows-[auto_1fr_auto] min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)] bg-gray-100">
      
      {/* Navbar */}
      <Navbar />

      {/* Main Content */}
      <main className="flex flex-col gap-8 row-start-2 items-center sm:items-start max-w-5xl w-full mx-auto">
        <h1 className="text-3xl font-bold mb-4">Latest News Clusters</h1>
        <ClusteredNews />
      </main>

      {/* Footer */}
      <footer className="row-start-3 flex flex-wrap items-center justify-center gap-6 text-sm text-gray-500 border-t pt-4 w-full">
        <p>Athul Rai</p>
        <a
          href="https://github.com/athul-rai"
          target="_blank"
          rel="noopener noreferrer"
          className="hover:underline"
        >
          GitHub
        </a>
        <a
          href="https://linkedin.com/in/athul-rai"
          target="_blank"
          rel="noopener noreferrer"
          className="hover:underline"
        >
          LinkedIn
        </a>
      </footer>
    </div>
  );
}
