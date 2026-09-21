import { apiFetch, authHeaders } from "@/services/api";
import type {
  Reminder,
  ReminderCreatePayload,
  ReminderListResponse,
  ReminderUpdatePayload,
} from "@/lib/types/reminders";

export function getReminders(token: string) {
  return apiFetch<ReminderListResponse>("/api/reminders", {
    headers: authHeaders(token),
  });
}

export const listReminders = getReminders;

export function createReminder(token: string, payload: ReminderCreatePayload) {
  return apiFetch<Reminder>("/api/reminders", {
    method: "POST",
    headers: authHeaders(token),
    body: JSON.stringify(payload),
  });
}

export function updateReminder(
  token: string,
  reminderId: number,
  payload: ReminderUpdatePayload,
) {
  return apiFetch<Reminder>(`/api/reminders/${reminderId}`, {
    method: "PUT",
    headers: authHeaders(token),
    body: JSON.stringify(payload),
  });
}

export function deleteReminder(token: string, reminderId: number) {
  return apiFetch<{ message: string; success: boolean }>(
    `/api/reminders/${reminderId}`,
    {
      method: "DELETE",
      headers: authHeaders(token),
    },
  );
}
