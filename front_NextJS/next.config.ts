import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  webpack: (config, { isServer }) => {
    config.module.rules.push({
      test: /\.svg$/,
      use: ["@svgr/webpack"],
    });

    if (!isServer) {
      config.watchOptions = {
        poll: 1000, // Vérifie les changements toutes les secondes
        aggregateTimeout: 300, // Temps avant de commencer à recompiler
      };
    }
    return config;
  },
};

export default nextConfig;

