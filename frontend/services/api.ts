import { API_TIMEOUT_MS, apiUrl } from "@/config/env";

export class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
    public body: string,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

export function authHeaders(token: string): HeadersInit {
  return {
    "Content-Type": "application/json",
    Authorization: `Bearer ${token}`,
  };
}

interface RequestOptions extends RequestInit {
  timeoutMs?: number;
}

export async function apiFetch<T>(
  path: string,
  options: RequestOptions = {},
): Promise<T> {
  const controller = new AbortController();
  const timeout = window.setTimeout(
    () => controller.abort(),
    options.timeoutMs ?? API_TIMEOUT_MS,
  );

  try {
    const response = await fetch(apiUrl(path), {
      ...options,
      signal: options.signal ?? controller.signal,
      headers: {
        "Content-Type": "application/json",
        ...(options.headers || {}),
      },
    });

    const raw = await response.text();
    if (!response.ok) {
      throw new ApiError(raw || response.statusText, response.status, raw);
    }

    return raw ? (JSON.parse(raw) as T) : (undefined as T);
  } finally {
    window.clearTimeout(timeout);
  }
}

export function getErrorMessage(error: unknown, fallback = "Request failed") {
  return error instanceof Error ? error.message : fallback;
}
