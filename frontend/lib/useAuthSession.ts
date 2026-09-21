"use client";

import { useCallback, useEffect, useState } from "react";

export interface AppUserProfile {
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

interface UseAuthSessionResult {
  token: string;
  user: AppUserProfile | null;
  sessionLoading: boolean;
  setSession: (nextToken: string, nextUser: AppUserProfile) => void;
  updateUser: (nextUser: AppUserProfile) => void;
  clearSession: () => void;
}

function authHeaders(authToken: string): HeadersInit {
  return {
    "Content-Type": "application/json",
    Authorization: `Bearer ${authToken}`,
  };
}

export function useAuthSession(): UseAuthSessionResult {
  const [token, setToken] = useState<string>("");
  const [user, setUser] = useState<AppUserProfile | null>(null);
  const [sessionLoading, setSessionLoading] = useState(true);

  const clearSession = useCallback(() => {
    localStorage.removeItem("gs_token");
    setToken("");
    setUser(null);
  }, []);

  const fetchMe = useCallback(async (authToken: string) => {
    const res = await fetch("/auth/me", {
      headers: authHeaders(authToken),
    });

    if (!res.ok) {
      return null;
    }

    return (await res.json()) as AppUserProfile;
  }, []);

  useEffect(() => {
    let active = true;

    const bootstrapSession = async () => {
      const saved = localStorage.getItem("gs_token");
      if (!saved) {
        if (active) {
          setSessionLoading(false);
        }
        return;
      }

      if (active) {
        setToken(saved);
      }

      const me = await fetchMe(saved);
      if (!active) return;

      if (!me) {
        clearSession();
      } else {
        setUser(me);
      }

      setSessionLoading(false);
    };

    void bootstrapSession();

    return () => {
      active = false;
    };
  }, [clearSession, fetchMe]);

  const setSession = useCallback(
    (nextToken: string, nextUser: AppUserProfile) => {
      localStorage.setItem("gs_token", nextToken);
      setToken(nextToken);
      setUser(nextUser);
    },
    [],
  );

  const updateUser = useCallback((nextUser: AppUserProfile) => {
    setUser(nextUser);
  }, []);

  return {
    token,
    user,
    sessionLoading,
    setSession,
    updateUser,
    clearSession,
  };
}
