import { apiUrl } from "@/config/env";
import { ApiError, apiFetch } from "@/services/api";
import type { ProfilePhotoResponse } from "@/lib/types/profileAssets";

export function getProfilePhoto(token: string) {
  return apiFetch<ProfilePhotoResponse>("/api/profile/photo", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
}

export const getProfilePhotoMeta = getProfilePhoto;

export async function uploadProfilePhoto(token: string, file: File) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(apiUrl("/api/profile/photo"), {
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

  return raw ? (JSON.parse(raw) as ProfilePhotoResponse) : null;
}

export function deleteProfilePhoto(token: string) {
  return apiFetch<ProfilePhotoResponse>("/api/profile/photo", {
    method: "DELETE",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
}

export function getProfilePhotoFileUrl() {
  return apiUrl("/api/profile/photo/file");
}

export async function getProfilePhotoFile(token: string) {
  const response = await fetch(apiUrl("/api/profile/photo/file"), {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    const raw = await response.text();
    throw new ApiError(raw || response.statusText, response.status, raw);
  }

  return response.blob();
}
