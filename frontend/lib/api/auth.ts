import { apiFetch, authHeaders } from "@/services/api";
import type {
  AuthResponse,
  LoginRequest,
  ProfileUpdateRequest,
  SignupRequest,
  UserProfile,
} from "@/lib/types/auth";

export function login(payload: LoginRequest) {
  return apiFetch<AuthResponse>("/auth/login", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function signup(payload: SignupRequest) {
  return apiFetch<AuthResponse>("/auth/signup", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function getMe(token: string) {
  return apiFetch<UserProfile>("/auth/me", {
    headers: authHeaders(token),
  });
}

export function updateProfile(token: string, payload: ProfileUpdateRequest) {
  return apiFetch<UserProfile>("/auth/profile", {
    method: "PUT",
    headers: authHeaders(token),
    body: JSON.stringify(payload),
  });
}
