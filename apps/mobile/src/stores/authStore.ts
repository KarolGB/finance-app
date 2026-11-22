import { create } from "zustand";
import api, {
  setSessionExpiredHandler,
  clearTokens,
  saveTokens,
} from "@/utils/api";
import { getItemAsync } from "expo-secure-store";
import axios from "axios";

type User = {
  id: string;
  email: string;
  first_name: string | null;
  last_name: string | null;
};

type authStore = {
  isAuthenticated: boolean;
  isLoading: boolean;
  user: User | null;
};

export const useAuthStore = create<authStore>(() => ({
  isAuthenticated: false,
  isLoading: true,
  user: null,
}));

export const initializeAuth = async () => {
  useAuthStore.setState({ isLoading: true });
  try {
    const token = await getItemAsync("authToken");
    if (!token) {
      useAuthStore.setState({
        isLoading: false,
        isAuthenticated: false,
        user: null,
      });
      return;
    }
    const { data } = await api.get<User>("/users/me");
    useAuthStore.setState({ isAuthenticated: true, user: data });
  } catch (err) {
    const status = axios.isAxiosError(err) ? err.response?.status : undefined;
    if (status === 401 || status == 403) {
      await clearTokens();
      useAuthStore.setState({ isAuthenticated: false, user: null });
    } else {
      useAuthStore.setState({ isAuthenticated: false });
    }
  } finally {
    useAuthStore.setState({ isLoading: false });
  }
};

export const login = async (email: string, password: string) => {
  const { data } = await api.post("/auth/login", {
    email: email,
    password: password,
  });
  const { access_token, refresh_token } = data;
  await saveTokens(access_token, refresh_token);
  const response = await api.get<User>("/users/me");
  useAuthStore.setState({ isAuthenticated: true, user: response.data });
};

export const register = async (
  email: string,
  password: string,
  first_name: string,
  last_name: string,
) => {
  const { data } = await api.post("/auth/register", {
    email: email,
    password: password,
    first_name: first_name,
    last_name: last_name,
  });
  const { access_token, refresh_token } = data;
  await saveTokens(access_token, refresh_token);
  const response = await api.get<User>("/users/me");
  useAuthStore.setState({ isAuthenticated: true, user: response.data });
};

export const logout = async () => {
  const refreshToken = await getItemAsync("refreshToken");
  if (refreshToken) {
    try {
      await api.post("/auth/logout", {
        refresh_token: refreshToken,
      });
    } catch {
      // Avoid network errors
    }
  }
  await clearTokens();
  useAuthStore.setState({ isAuthenticated: false, user: null });
};

setSessionExpiredHandler(() => {
  useAuthStore.setState({ isAuthenticated: false, user: null });
});
