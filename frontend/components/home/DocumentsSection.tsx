"use client";

import { ChangeEvent, useEffect, useState } from "react";
import {
  deleteDocument,
  downloadDocument,
  listDocuments,
  uploadDocument,
} from "@/lib/api/documents";
import type { DocumentType, UserDocument } from "@/lib/types/documents";

const DOCUMENT_TYPES: DocumentType[] = [
  "aadhaar_card",
  "pan_card",
  "income_certificate",
  "caste_certificate",
  "disability_certificate",
  "land_documents",
  "other",
];

function formatBytes(bytes: number) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

export default function DocumentsSection({ token }: { token: string }) {
  const [items, setItems] = useState<UserDocument[]>([]);
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [selectedType, setSelectedType] = useState<DocumentType>("other");
  const [error, setError] = useState("");

  async function loadItems() {
    setLoading(true);
    setError("");
    try {
      if (!token) {
        setItems([]);
        return;
      }
      const data = await listDocuments(token);
      setItems(data.documents);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to load documents");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void loadItems();
  }, [token]);

  async function handleUpload(e: ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploading(true);
    setError("");
    try {
      const result = await uploadDocument(token, selectedType, file);
      if (result?.document) {
        setItems((prev) => [result.document, ...prev]);
      }
    } catch (err: unknown) {
      setError(
        err instanceof Error ? err.message : "Failed to upload document",
      );
    } finally {
      setUploading(false);
      e.target.value = "";
    }
  }

  async function handleDelete(documentId: number) {
    try {
      await deleteDocument(token, documentId);
      setItems((prev) => prev.filter((item) => item.id !== documentId));
    } catch (err: unknown) {
      setError(
        err instanceof Error ? err.message : "Failed to delete document",
      );
    }
  }

  return (
    <section className="bg-white rounded-2xl border border-orange-100 shadow-sm p-6">
      <h2 className="text-xl font-bold text-gray-800">My Documents</h2>
      <p className="text-sm text-gray-500 mt-1">
        Upload required documents for faster scheme applications
      </p>

      <div className="mt-4 flex flex-wrap items-center gap-3">
        <select
          value={selectedType}
          onChange={(e) => setSelectedType(e.target.value as DocumentType)}
          className="border border-gray-300 rounded-lg px-3 py-2 text-sm"
        >
          {DOCUMENT_TYPES.map((type) => (
            <option key={type} value={type}>
              {type.replace(/_/g, " ")}
            </option>
          ))}
        </select>
        <label className="text-sm px-4 py-2 rounded-lg border border-blue-300 bg-blue-50 text-blue-700 hover:bg-blue-100 cursor-pointer">
          {uploading ? "Uploading..." : "Upload document"}
          <input
            type="file"
            className="hidden"
            onChange={(e) => void handleUpload(e)}
            accept=".pdf,.png,.jpg,.jpeg,.webp"
            disabled={uploading}
          />
        </label>
      </div>

      {error && <p className="text-sm text-red-600 mt-3">{error}</p>}
      {loading && (
        <p className="text-sm text-gray-500 mt-4">Loading documents...</p>
      )}

      {!loading && (
        <div className="mt-5 space-y-2">
          {items.length === 0 && (
            <p className="text-sm text-gray-500">No documents uploaded yet.</p>
          )}
          {items.map((item) => (
            <div
              key={item.id}
              className="flex items-center justify-between gap-3 rounded-xl border border-gray-200 px-3 py-2"
            >
              <div>
                <p className="text-sm font-semibold text-gray-800">
                  {item.original_name}
                </p>
                <p className="text-xs text-gray-500">
                  {item.document_type.replace(/_/g, " ")} •{" "}
                  {formatBytes(item.file_size)}
                </p>
              </div>
              <div className="flex items-center gap-2">
                <button
                  type="button"
                  onClick={() =>
                    void downloadDocument(token, item.id, item.original_name)
                  }
                  className="text-xs px-2 py-1 rounded border border-gray-300"
                >
                  Download
                </button>
                <button
                  type="button"
                  onClick={() => void handleDelete(item.id)}
                  className="text-xs px-2 py-1 rounded border border-red-200 text-red-600"
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}
