/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: false,
  swcMinify: true,

  // Optimize build performance for Vercel
  experimental: {
    optimizeCss: false, // Disable CSS optimization to speed up builds
    webVitalsAttribution: ["CLS", "LCP"], // Only track essential web vitals
  },

  // Faster builds
  compiler: {
    // Remove console.log in production builds
    removeConsole: process.env.NODE_ENV === "production",
  },

  // Optimize images for better performance
  images: {
    domains: [],
    formats: ["image/webp", "image/avif"],
    unoptimized: true, // Disable image optimization to speed up builds
  },

  // Disable some optimizations that slow down builds
  compress: true,
  poweredByHeader: false,

  // Skip type checking during build (rely on CI/CD for type checks)
  typescript: {
    ignoreBuildErrors: false,
  },

  // Skip ESLint during builds to speed up deployment
  eslint: {
    ignoreDuringBuilds: true,
  },

  // Optimize output
  output: "standalone",

  // Security headers (simplified to reduce build complexity)
  async headers() {
    return [
      {
        source: "/(.*)",
        headers: [
          {
            key: "X-Content-Type-Options",
            value: "nosniff",
          },
          {
            key: "X-Frame-Options",
            value: "DENY",
          },
        ],
      },
    ];
  },
};

module.exports = nextConfig;
