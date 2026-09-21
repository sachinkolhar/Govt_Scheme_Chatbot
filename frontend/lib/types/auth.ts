export interface UserProfile {
  id: number;
  username: string;
  name: string;
  age: number | null;
  gender: string | null;
  state: string | null;
  occupation: string | null;
  income: number | null;
  category: string | null;
  disability: boolean;
  student_status: boolean;
  farmer_status: boolean;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface SignupRequest extends LoginRequest {
  name: string;
}

export type ProfileUpdateRequest = Omit<UserProfile, "id" | "username">;

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: UserProfile;
}
