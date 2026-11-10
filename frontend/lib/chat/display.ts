import type { Scheme } from "@/lib/types/schemes";

export function appendStreamToken(content: string, token: string): string {
  return content + token;
}

export function getDistinctRelevantSchemes(
  primary: Scheme | undefined,
  relevant: Scheme[] | undefined,
): Scheme[] {
  if (!relevant) return [];
  if (!primary) return relevant;

  const primaryName = primary.scheme_name.trim().toLocaleLowerCase();
  return relevant.filter(
    (scheme) => scheme.scheme_name.trim().toLocaleLowerCase() !== primaryName,
  );
}
