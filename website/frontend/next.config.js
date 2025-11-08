/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: false,
  swcMinify: true,
  // Remove rewrites for production - API calls should go directly to backend URL
  // async rewrites() {
  //   return [
  //     {
  //       source: "/api/:path*",
  //       destination: "http://localhost:5000/api/:path*",
  //     },
  //   ];
  // },

  // Optional: Enable static export if needed for certain hosting platforms
  // trailingSlash: true,
  // output: 'export',

  // Optimize images for better performance
  images: {
    domains: [],
    formats: ["image/webp", "image/avif"],
  },

  // Compression and performance
  compress: true,

  // Security headers
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
          {
            key: "X-XSS-Protection",
            value: "1; mode=block",
          },
        ],
      },
    ];
  },
};

module.exports = nextConfig;
