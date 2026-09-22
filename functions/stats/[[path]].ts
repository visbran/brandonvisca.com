/**
 * First-party proxy for Tianji analytics.
 *
 * The browser only ever talks to brandonvisca.com/stats/*. This function
 * forwards the three tracker paths to Tianji through a Cloudflare Tunnel
 * protected by Cloudflare Access (service token), so the Tianji instance
 * itself is never reachable from the Internet.
 *
 * Required Cloudflare Pages environment variables:
 *   TIANJI_ORIGIN            e.g. https://tianji-ingest.brandonvisca.com
 *   CF_ACCESS_CLIENT_ID      Access service token id
 *   CF_ACCESS_CLIENT_SECRET  Access service token secret (encrypted)
 */

interface Env {
  TIANJI_ORIGIN?: string;
  CF_ACCESS_CLIENT_ID?: string;
  CF_ACCESS_CLIENT_SECRET?: string;
}

interface Context {
  request: Request;
  env: Env;
  params: { path?: string | string[] };
}

// Only the tracker surface is proxied — never the admin UI or other APIs.
const ALLOWED = new Map<string, string[]>([
  ["tracker.js", ["GET", "HEAD"]],
  ["api/website/send", ["POST"]],
  ["api/website/batch", ["POST"]],
]);

export async function onRequest({ request, env, params }: Context) {
  const path = Array.isArray(params.path)
    ? params.path.join("/")
    : (params.path ?? "");
  const methods = ALLOWED.get(path);

  if (!methods) return new Response("Not found", { status: 404 });
  if (!methods.includes(request.method)) {
    return new Response("Method not allowed", {
      status: 405,
      headers: { Allow: methods.join(", ") },
    });
  }
  if (
    !env.TIANJI_ORIGIN ||
    !env.CF_ACCESS_CLIENT_ID ||
    !env.CF_ACCESS_CLIENT_SECRET
  ) {
    return new Response("Analytics not configured", { status: 503 });
  }

  const headers = new Headers();
  for (const name of ["content-type", "user-agent", "accept-language"]) {
    const value = request.headers.get(name);
    if (value) headers.set(name, value);
  }
  // Subrequests leave from Cloudflare's IP: pass the visitor's IP on so
  // Tianji can resolve the country. It is not stored in clear by Tianji.
  const ip = request.headers.get("cf-connecting-ip");
  if (ip) headers.set("x-forwarded-for", ip);
  headers.set("CF-Access-Client-Id", env.CF_ACCESS_CLIENT_ID);
  headers.set("CF-Access-Client-Secret", env.CF_ACCESS_CLIENT_SECRET);

  const upstream = await fetch(
    `${env.TIANJI_ORIGIN.replace(/\/$/, "")}/${path}`,
    {
      method: request.method,
      headers,
      body: request.method === "POST" ? request.body : undefined,
    }
  );

  const response = new Response(upstream.body, upstream);
  response.headers.delete("set-cookie");
  if (path === "tracker.js") {
    response.headers.set("cache-control", "public, max-age=3600");
  } else {
    response.headers.set("cache-control", "no-store");
  }
  return response;
}
