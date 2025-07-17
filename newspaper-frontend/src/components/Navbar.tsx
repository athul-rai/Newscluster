"use client";

import Link from "next/link";

export default function Navbar() {
  return (
    <nav className="flex items-center justify-between px-6 py-4 bg-gray-900 text-white shadow">
      <Link href="/">
        <span className="text-2xl font-bold tracking-wide hover:text-blue-400 transition">
          NewsCluster
        </span>
      </Link>

      <div className="space-x-4">
        {/* Future buttons/links */}
        {/* Dashboard button removed */}
      </div>
    </nav>
  );
}
