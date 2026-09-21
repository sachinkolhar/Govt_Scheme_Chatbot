export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL?.replace(/\/$/, "") || "";

export const API_TIMEOUT_MS = Number(
  process.env.NEXT_PUBLIC_API_TIMEOUT_MS || 30000,
);

export function apiUrl(path: string) {
  const normalized = path.startsWith("/") ? path : `/${path}`;
  return `${API_BASE_URL}${normalized}`;
}
