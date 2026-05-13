type ApiErrorLike = {
  detail?: unknown;
  error?: unknown;
  message?: unknown;
};

function stringifyMessage(value: unknown): string | null {
  if (typeof value === "string" && value.trim()) return value;
  if (Array.isArray(value) && value.length > 0) {
    return value.map(item => stringifyMessage(item) ?? JSON.stringify(item)).join(", ");
  }
  if (value && typeof value === "object") {
    try {
      return JSON.stringify(value);
    } catch {
      return null;
    }
  }
  return null;
}

export function apiErrorMessage(data: unknown, fallback = "İşlem tamamlanamadı."): string {
  if (!data || typeof data !== "object") return fallback;

  const source = data as ApiErrorLike;
  return (
    stringifyMessage(source.detail) ??
    stringifyMessage(source.error) ??
    stringifyMessage(source.message) ??
    fallback
  );
}
