export type ReminderType = "deadline" | "saved_event" | "custom";

export interface Reminder {
  id: number;
  user_id: number;
  title: string;
  description?: string | null;
  reminder_date: string;
  related_scheme_name?: string | null;
  reminder_type: ReminderType;
  created_at: string;
  updated_at: string;
}

export interface ReminderCreatePayload {
  title: string;
  description?: string;
  reminder_date: string;
  related_scheme_name?: string;
  reminder_type?: ReminderType;
}

export interface ReminderUpdatePayload {
  title?: string;
  description?: string;
  reminder_date?: string;
  related_scheme_name?: string;
  reminder_type?: ReminderType;
}

export interface ReminderListResponse {
  reminders: Reminder[];
  total_count: number;
}
