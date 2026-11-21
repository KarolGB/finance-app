import axios, { AxiosError, InternalAxiosRequestConfig } from "axios";
import { getItemAsync, setItemAsync, deleteItemAsync } from "expo-secure-store";
import { createMMKV } from "react-native-mmkv";
import { DEFAULT_API_URL } from "@/utils/constants";

const apiStorage = createMMKV({
  id: "api",
});

const api = axios.create({
  baseURL: apiStorage.getString("API_URL") || DEFAULT_API_URL,
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
});

let accessToken: string | null = null;
let refreshPromise: Promise<string> | null = null;
let onSessionExpired: (() => void) | null = null;
type RetriableConfig = InternalAxiosRequestConfig & { _retry?: boolean };

export function setApiUrl(url: string) {
  const clean = url.trim().replace(/\/+$/, "");
  apiStorage.set("API_URL", clean);
  api.defaults.baseURL = clean;
}

export async function clearTokens() {
  accessToken = null;
  await Promise.all([
    deleteItemAsync("authToken"),
    deleteItemAsync("refreshToken"),
  ]);
}

export async function saveTokens(access: string, refresh: string) {
  accessToken = access;
  await Promise.all([
    setItemAsync("authToken", access),
    setItemAsync("refreshToken", refresh),
  ]);
}

export const setSessionExpiredHandler = (fn: () => void) => {
  onSessionExpired = fn;
};

async function refreshAccessToken(): Promise<string> {
  const refreshToken = await getItemAsync("refreshToken");
  if (!refreshToken) throw new Error("NO_REFRESH_TOKEN");

  const { data } = await axios.post(
    `${api.defaults.baseURL}/auth/refresh`,
    { refresh_token: refreshToken },
    { timeout: 10000 },
  );
  await setItemAsync("authToken", data.access_token);
  await setItemAsync("refreshToken", data.refresh_token);
  return data.access_token;
}

api.interceptors.request.use(
  async (config) => {
    if (accessToken === null) {
      accessToken = await getItemAsync("authToken");
    }
    if (accessToken) {
      config.headers["Authorization"] = `Bearer ${accessToken}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);

api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as RetriableConfig | undefined;
    const isAuthRoute = originalRequest?.url?.includes("/auth/");
    if (
      error.response?.status !== 401 ||
      !originalRequest ||
      originalRequest._retry ||
      isAuthRoute
    ) {
      return Promise.reject(error);
    }
    originalRequest._retry = true;

    try {
      refreshPromise ??= refreshAccessToken().finally(() => {
        refreshPromise = null;
      });
      const newToken = await refreshPromise;
      accessToken = newToken;
      originalRequest.headers.Authorization = `Bearer ${newToken}`;
      return api(originalRequest);
    } catch (refreshError) {
      const status = axios.isAxiosError(refreshError)
        ? refreshError.response?.status
        : undefined;
      const noToken =
        refreshError instanceof Error &&
        refreshError.message === "NO_REFRESH_TOKEN";
      if (noToken || status === 401 || status === 403) {
        await clearTokens();
        onSessionExpired?.();
      }
      return Promise.reject(error);
    }
  },
);

export default api;
