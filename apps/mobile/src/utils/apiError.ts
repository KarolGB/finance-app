import { isAxiosError } from "axios";
export default function getFastApiErrorMessage(
  err: unknown,
  fallback: string,
): string {
  if (isAxiosError(err)) {
    const detail = err.response?.data?.detail;
    if (typeof detail === "string") return detail;
    if (Array.isArray(detail) && detail.length > 0) {
      return detail[0].msg;
    }
  }
  if (err instanceof Error && err.message) return err.message;
  return fallback;
}
