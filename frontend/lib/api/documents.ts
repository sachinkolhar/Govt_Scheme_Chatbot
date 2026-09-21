import { apiUrl } from "@/config/env";
import { ApiError, apiFetch, authHeaders } from "@/services/api";
import type {
  DocumentType,
  DocumentUploadResponse,
  UserDocumentListResponse,
} from "@/lib/types/documents";

export function getDocuments(token: string) {
  return apiFetch<UserDocumentListResponse>("/api/documents", {
    headers: authHeaders(token),
  });
}

export const listDocuments = getDocuments;

export async function uploadDocument(
  token: string,
  documentType: DocumentType,
  file: File,
) {
  const formData = new FormData();
  formData.append("document_type", documentType);
  formData.append("file", file);

  const response = await fetch(apiUrl("/api/documents"), {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
    },
    body: formData,
  });

  const raw = await response.text();
  if (!response.ok) {
    throw new ApiError(raw || response.statusText, response.status, raw);
  }

  return raw ? (JSON.parse(raw) as DocumentUploadResponse) : null;
}

export function deleteDocument(token: string, documentId: number) {
  return apiFetch<{ message: string; success: boolean }>(
    `/api/documents/${documentId}`,
    {
      method: "DELETE",
      headers: authHeaders(token),
    },
  );
}

export function getDocumentDownloadUrl(documentId: number) {
  return apiUrl(`/api/documents/${documentId}/download`);
}

export async function downloadDocument(
  token: string,
  documentId: number,
  originalName: string,
) {
  const response = await fetch(
    apiUrl(`/api/documents/${documentId}/download`),
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    },
  );

  if (!response.ok) {
    const raw = await response.text();
    throw new ApiError(raw || response.statusText, response.status, raw);
  }

  const blob = await response.blob();
  const objectUrl = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = objectUrl;
  anchor.download = originalName;
  document.body.appendChild(anchor);
  anchor.click();
  anchor.remove();
  URL.revokeObjectURL(objectUrl);
}
