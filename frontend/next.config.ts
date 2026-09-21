import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Proxy frontend routes to FastAPI backend on port 8000.
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: "http://127.0.0.1:8000/api/:path*",
      },
      {
        source: "/auth/:path*",
        destination: "http://127.0.0.1:8000/auth/:path*",
      },
      {
        source: "/health",
        destination: "http://127.0.0.1:8000/health",
      },
    ];
  },
};

export default nextConfig;
