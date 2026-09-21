"use client";

import { FormEvent, useEffect, useState } from "react";
import {
  createReminder,
  deleteReminder,
  listReminders,
  updateReminder,
} from "@/lib/api/reminders";
import type {
  Reminder,
  ReminderCreatePayload,
  ReminderType,
  ReminderUpdatePayload,
} from "@/lib/types/reminders";

type ReminderEditState = Record<number, ReminderUpdatePayload>;

const REMINDER_TYPES: ReminderType[] = ["deadline", "saved_event", "custom"];

function toDatetimeLocalValue(value: string) {
  return value ? value.slice(0, 16) : "";
}

export default function RemindersSection({ token }: { token: string }) {
  const [items, setItems] = useState<Reminder[]>([]);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [form, setForm] = useState<ReminderCreatePayload>({
    title: "",
    description: "",
    reminder_date: "",
    related_scheme_name: "",
    reminder_type: "custom",
  });
  const [editing, setEditing] = useState<ReminderEditState>({});

  async function loadItems() {
    setLoading(true);
    setError("");
    try {
      if (!token) {
        setItems([]);
        return;
      }
      const data = await listReminders(token);
      setItems(data.reminders);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to load reminders");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void loadItems();
  }, [token]);

  async function handleCreate(e: FormEvent) {
    e.preventDefault();
    if (!form.title.trim() || !form.reminder_date) return;

    setSaving(true);
    setError("");

    try {
      const created = await createReminder(token, {
        title: form.title,
        description: form.description?.trim() || undefined,
        reminder_date: new Date(form.reminder_date).toISOString(),
        related_scheme_name: form.related_scheme_name?.trim() || undefined,
        reminder_type: form.reminder_type || "custom",
      });

      setItems((prev) => [created, ...prev]);
      setForm({
        title: "",
        description: "",
        reminder_date: "",
        related_scheme_name: "",
        reminder_type: "custom",
      });
    } catch (err: unknown) {
      setError(
        err instanceof Error ? err.message : "Failed to create reminder",
      );
    } finally {
      setSaving(false);
    }
  }

  function startEdit(reminder: Reminder) {
    setEditing((prev) => ({
      ...prev,
      [reminder.id]: {
        title: reminder.title,
        description: reminder.description || "",
        reminder_date: toDatetimeLocalValue(reminder.reminder_date),
        related_scheme_name: reminder.related_scheme_name || "",
        reminder_type: reminder.reminder_type,
      },
    }));
  }

  function cancelEdit(reminderId: number) {
    setEditing((prev) => {
      const next = { ...prev };
      delete next[reminderId];
      return next;
    });
  }

  async function saveEdit(reminderId: number) {
    const patch = editing[reminderId];
    if (!patch) return;

    try {
      const updated = await updateReminder(token, reminderId, {
        ...patch,
        reminder_date: patch.reminder_date
          ? new Date(patch.reminder_date).toISOString()
          : undefined,
      });
      setItems((prev) =>
        prev.map((item) => (item.id === reminderId ? updated : item)),
      );
      cancelEdit(reminderId);
    } catch (err: unknown) {
      setError(
        err instanceof Error ? err.message : "Failed to update reminder",
      );
    }
  }

  async function removeReminder(reminderId: number) {
    try {
      await deleteReminder(token, reminderId);
      setItems((prev) => prev.filter((item) => item.id !== reminderId));
    } catch (err: unknown) {
      setError(
        err instanceof Error ? err.message : "Failed to delete reminder",
      );
    }
  }

  return (
    <section className="bg-white rounded-2xl border border-orange-100 shadow-sm p-6">
      <h2 className="text-xl font-bold text-gray-800">Reminders</h2>
      <p className="text-sm text-gray-500 mt-1">
        Track deadlines and important scheme events
      </p>

      <form onSubmit={handleCreate} className="mt-4 grid md:grid-cols-2 gap-3">
        <input
          value={form.title}
          onChange={(e) =>
            setForm((prev) => ({ ...prev, title: e.target.value }))
          }
          placeholder="Reminder title"
          className="border border-gray-300 rounded-lg px-3 py-2"
          required
        />
        <input
          type="datetime-local"
          value={form.reminder_date}
          onChange={(e) =>
            setForm((prev) => ({ ...prev, reminder_date: e.target.value }))
          }
          className="border border-gray-300 rounded-lg px-3 py-2"
          required
        />
        <input
          value={form.related_scheme_name}
          onChange={(e) =>
            setForm((prev) => ({
              ...prev,
              related_scheme_name: e.target.value,
            }))
          }
          placeholder="Related scheme (optional)"
          className="border border-gray-300 rounded-lg px-3 py-2"
        />
        <select
          value={form.reminder_type}
          onChange={(e) =>
            setForm((prev) => ({
              ...prev,
              reminder_type: e.target.value as ReminderType,
            }))
          }
          className="border border-gray-300 rounded-lg px-3 py-2"
        >
          {REMINDER_TYPES.map((type) => (
            <option key={type} value={type}>
              {type.replace("_", " ")}
            </option>
          ))}
        </select>
        <textarea
          value={form.description}
          onChange={(e) =>
            setForm((prev) => ({ ...prev, description: e.target.value }))
          }
          placeholder="Description (optional)"
          className="border border-gray-300 rounded-lg px-3 py-2 md:col-span-2"
          rows={2}
        />
        <div className="md:col-span-2">
          <button
            type="submit"
            disabled={saving}
            className="bg-orange-500 hover:bg-orange-600 text-white px-4 py-2 rounded-lg"
          >
            {saving ? "Saving..." : "Add reminder"}
          </button>
        </div>
      </form>

      {error && <p className="text-sm text-red-600 mt-3">{error}</p>}
      {loading && (
        <p className="text-sm text-gray-500 mt-4">Loading reminders...</p>
      )}

      {!loading && (
        <div className="mt-5 space-y-3">
          {items.length === 0 && (
            <p className="text-sm text-gray-500">No reminders yet.</p>
          )}

          {items.map((item) => {
            const draft = editing[item.id];
            const isEditing = Boolean(draft);

            return (
              <div
                key={item.id}
                className="border border-gray-200 rounded-xl p-3"
              >
                {isEditing ? (
                  <div className="grid md:grid-cols-2 gap-2">
                    <input
                      value={draft?.title || ""}
                      onChange={(e) =>
                        setEditing((prev) => ({
                          ...prev,
                          [item.id]: {
                            ...prev[item.id],
                            title: e.target.value,
                          },
                        }))
                      }
                      className="border border-gray-300 rounded-lg px-3 py-2"
                    />
                    <input
                      type="datetime-local"
                      value={draft?.reminder_date || ""}
                      onChange={(e) =>
                        setEditing((prev) => ({
                          ...prev,
                          [item.id]: {
                            ...prev[item.id],
                            reminder_date: e.target.value,
                          },
                        }))
                      }
                      className="border border-gray-300 rounded-lg px-3 py-2"
                    />
                    <input
                      value={draft?.related_scheme_name || ""}
                      onChange={(e) =>
                        setEditing((prev) => ({
                          ...prev,
                          [item.id]: {
                            ...prev[item.id],
                            related_scheme_name: e.target.value,
                          },
                        }))
                      }
                      className="border border-gray-300 rounded-lg px-3 py-2"
                      placeholder="Related scheme"
                    />
                    <select
                      value={draft?.reminder_type || "custom"}
                      onChange={(e) =>
                        setEditing((prev) => ({
                          ...prev,
                          [item.id]: {
                            ...prev[item.id],
                            reminder_type: e.target.value as ReminderType,
                          },
                        }))
                      }
                      className="border border-gray-300 rounded-lg px-3 py-2"
                    >
                      {REMINDER_TYPES.map((type) => (
                        <option key={type} value={type}>
                          {type.replace("_", " ")}
                        </option>
                      ))}
                    </select>
                    <textarea
                      value={draft?.description || ""}
                      onChange={(e) =>
                        setEditing((prev) => ({
                          ...prev,
                          [item.id]: {
                            ...prev[item.id],
                            description: e.target.value,
                          },
                        }))
                      }
                      rows={2}
                      className="md:col-span-2 border border-gray-300 rounded-lg px-3 py-2"
                    />
                    <div className="md:col-span-2 flex gap-2">
                      <button
                        type="button"
                        onClick={() => void saveEdit(item.id)}
                        className="text-sm px-3 py-1.5 rounded-lg bg-blue-600 text-white"
                      >
                        Save
                      </button>
                      <button
                        type="button"
                        onClick={() => cancelEdit(item.id)}
                        className="text-sm px-3 py-1.5 rounded-lg border border-gray-300"
                      >
                        Cancel
                      </button>
                    </div>
                  </div>
                ) : (
                  <div>
                    <div className="flex items-start justify-between gap-3">
                      <div>
                        <h3 className="font-semibold text-gray-800">
                          {item.title}
                        </h3>
                        <p className="text-xs text-gray-500 mt-1">
                          {new Date(item.reminder_date).toLocaleString()} •{" "}
                          {item.reminder_type}
                        </p>
                        {item.related_scheme_name && (
                          <p className="text-xs text-orange-700 mt-1">
                            Scheme: {item.related_scheme_name}
                          </p>
                        )}
                      </div>
                      <div className="flex gap-2">
                        <button
                          type="button"
                          onClick={() => startEdit(item)}
                          className="text-xs px-2 py-1 rounded border border-gray-300"
                        >
                          Edit
                        </button>
                        <button
                          type="button"
                          onClick={() => void removeReminder(item.id)}
                          className="text-xs px-2 py-1 rounded border border-red-200 text-red-600"
                        >
                          Delete
                        </button>
                      </div>
                    </div>
                    {item.description && (
                      <p className="text-sm text-gray-700 mt-2">
                        {item.description}
                      </p>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </section>
  );
}
