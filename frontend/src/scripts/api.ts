import { BACKEND_URL, ACCESS_TOKEN, REFRESH_TOKEN } from "./config";
import axios from "axios";
import { ref } from "vue";

const api = axios.create({
  baseURL: BACKEND_URL,
});

export const isAuthenticated = ref(false);

api.interceptors.request.use((config) => {
  const token = localStorage.getItem(ACCESS_TOKEN);
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (config) => config,
  async (error) => {
    if (error.response?.status === 401 && !error.config._retry) {
      error.config._retry = true;
      return refreshToken()
        .then(() => {
          return api(error.config);
        })
        .catch((error) => Promise.reject(error));
    }
    return Promise.reject(error);
  },
);

export async function refreshToken() {
  const refreshToken = localStorage.getItem(REFRESH_TOKEN);

  return axios
    .post(`${BACKEND_URL}/api/token/refresh/`, {
      refresh: refreshToken,
    })
    .then((response) => {
      localStorage.setItem(ACCESS_TOKEN, response.data.access);
      isAuthenticated.value = true;
    })
    .catch((error) => {
      isAuthenticated.value = false;
      return Promise.reject(error);
    });
}

export default api;
