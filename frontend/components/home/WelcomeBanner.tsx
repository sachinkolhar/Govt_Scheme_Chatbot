"use client";

import { ChangeEvent, useEffect, useState } from "react";
import {
  deleteProfilePhoto,
  getProfilePhotoFile,
  getProfilePhotoMeta,
  uploadProfilePhoto,
} from "@/lib/api/profileAssets";

export default function WelcomeBanner({
  greetingName,
  token,
}: {
  greetingName: string;
  token: string;
}) {
  const [photoUrl, setPhotoUrl] = useState<string | null>(null);
  const [hasPhoto, setHasPhoto] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function loadPhoto() {
    setLoading(true);
    setError("");
    try {
      if (!token) {
        setHasPhoto(false);
        setPhotoUrl((prev) => {
          if (prev) URL.revokeObjectURL(prev);
          return null;
        });
        return;
      }

      const meta = await getProfilePhotoMeta(token);
      const nextHasPhoto = Boolean(meta.profile_photo_path);
      setHasPhoto(nextHasPhoto);

      if (nextHasPhoto) {
        const blob = await getProfilePhotoFile(token);
        setPhotoUrl((prev) => {
          if (prev) URL.revokeObjectURL(prev);
          return URL.createObjectURL(blob);
        });
      } else {
        setPhotoUrl((prev) => {
          if (prev) URL.revokeObjectURL(prev);
          return null;
        });
      }
    } catch (err: unknown) {
      setError(
        err instanceof Error ? err.message : "Failed to load profile photo",
      );
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void loadPhoto();
    return () => {
      setPhotoUrl((prev) => {
        if (prev) URL.revokeObjectURL(prev);
        return null;
      });
    };
  }, [token]);

  async function handleUpload(e: ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;

    try {
      await uploadProfilePhoto(token, file);
      await loadPhoto();
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to upload photo");
    } finally {
      e.target.value = "";
    }
  }

  async function handleDelete() {
    try {
      await deleteProfilePhoto(token);
      await loadPhoto();
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to delete photo");
    }
  }

  return (
    <section className="bg-gradient-to-r from-orange-100 via-white to-green-100 rounded-2xl border border-orange-200 shadow-sm p-6">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center gap-4">
          <div className="h-16 w-16 rounded-full bg-white border border-orange-200 overflow-hidden grid place-items-center">
            {photoUrl ? (
              <img
                src={photoUrl}
                alt="Profile"
                className="h-full w-full object-cover"
              />
            ) : (
              <span className="text-xl font-bold text-orange-600">
                {greetingName.slice(0, 1).toUpperCase()}
              </span>
            )}
          </div>
          <div>
            <h2 className="text-lg font-bold text-gray-800">
              Welcome back, {greetingName}!
            </h2>
            <p className="text-sm text-gray-600">
              Manage your profile, reminders, and documents in one place.
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <label className="text-sm px-3 py-2 rounded-lg border border-blue-300 bg-blue-50 text-blue-700 hover:bg-blue-100 cursor-pointer">
            Upload photo
            <input
              type="file"
              className="hidden"
              accept=".png,.jpg,.jpeg,.webp"
              onChange={(e) => void handleUpload(e)}
              disabled={loading}
            />
          </label>
          {hasPhoto && (
            <button
              type="button"
              onClick={() => void handleDelete()}
              className="text-sm px-3 py-2 rounded-lg border border-red-300 text-red-700 hover:bg-red-50"
            >
              Remove
            </button>
          )}
        </div>
      </div>
      {error && <p className="text-sm text-red-600 mt-3">{error}</p>}
    </section>
  );
}
