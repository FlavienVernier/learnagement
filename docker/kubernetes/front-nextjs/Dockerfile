FROM node:26-bookworm-slim AS build

WORKDIR /app
COPY front_NextJS/package.json front_NextJS/package-lock.json ./
RUN npm ci --no-audit --no-fund
COPY front_NextJS/ ./
RUN npm run build \
    && npm prune --omit=dev --no-audit --no-fund

FROM node:26-bookworm-slim

ENV NODE_ENV=production \
    NEXT_TELEMETRY_DISABLED=1

WORKDIR /app
COPY --from=build --chown=node:node /app/package.json /app/package-lock.json ./
COPY --from=build --chown=node:node /app/node_modules ./node_modules
COPY --from=build --chown=node:node /app/.next ./.next
COPY --from=build --chown=node:node /app/public ./public
COPY --from=build --chown=node:node /app/next.config.ts ./next.config.ts

USER node
EXPOSE 3000
STOPSIGNAL SIGTERM

CMD ["npm", "run", "start", "--", "--hostname", "0.0.0.0"]
