import { apiFetch } from "@/services/api";
import type {
  TranslateRequest,
  TranslateResponse,
  SpeakRequest,
  SpeakResponse,
  IVRScheme,
} from "@/lib/types/ivr";

export async function translateText(
  request: TranslateRequest,
): Promise<TranslateResponse> {
  return apiFetch<TranslateResponse>("/api/ivr/translate", {
    method: "POST",
    body: JSON.stringify(request),
  });
}

export async function speakText(request: SpeakRequest): Promise<SpeakResponse> {
  return apiFetch<SpeakResponse>("/api/ivr/speak", {
    method: "POST",
    body: JSON.stringify(request),
  });
}

export async function getDemoScheme(): Promise<IVRScheme> {
  return apiFetch<IVRScheme>("/api/ivr/scheme/demo", {
    method: "GET",
  });
}

export async function getAvailableLanguages(): Promise<Record<string, string>> {
  return apiFetch<Record<string, string>>("/api/ivr/languages", {
    method: "GET",
  });
}

export function audioBase64ToBlob(base64String: string): Blob {
  try {
    if (!base64String || typeof base64String !== "string") {
      throw new Error("Invalid base64 string");
    }

    // Remove any whitespace and data URI prefix if present
    let cleanBase64 = base64String.trim();
    if (cleanBase64.startsWith("data:")) {
      cleanBase64 = cleanBase64.split(",")[1];
    }

    // Decode base64 to binary string
    const binaryString = atob(cleanBase64);

    // Convert binary string to Uint8Array
    const bytes = new Uint8Array(binaryString.length);
    for (let i = 0; i < binaryString.length; i++) {
      bytes[i] = binaryString.charCodeAt(i);
    }

    // Create blob with correct MIME type for MP3
    const blob = new Blob([bytes], { type: "audio/mpeg" });

    console.log(`Created audio blob: ${blob.size} bytes, type: ${blob.type}`);

    return blob;
  } catch (error) {
    console.error("Error converting base64 to blob:", error);
    throw error;
  }
}
