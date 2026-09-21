export function validateSignupPassword(rawPassword: string): string | null {
  if (rawPassword.length < 8) {
    return "Password must be at least 8 characters long.";
  }
  if (!/[A-Z]/.test(rawPassword)) {
    return "Password must include at least 1 uppercase letter.";
  }
  if (!/\d/.test(rawPassword)) {
    return "Password must include at least 1 number.";
  }
  if (!/[^A-Za-z0-9]/.test(rawPassword)) {
    return "Password must include at least 1 special character.";
  }
  if (new TextEncoder().encode(rawPassword).length > 72) {
    return "Password is too long. Please keep your password to 72 characters or fewer.";
  }
  return null;
}

export function usePasswordValidation() {
  return { validateSignupPassword };
}
