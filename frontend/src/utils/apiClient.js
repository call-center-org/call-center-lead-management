import axios from "axios";
import { API_CONFIG } from "./apiConfig";
import { getToken, clearToken } from "./tokenManager";

// 创建 axios 实例
const apiClient = axios.create({
  baseURL: API_CONFIG.BASE_URL,
  timeout: API_CONFIG.TIMEOUT,
  headers: {
    "Content-Type": "application/json",
  },
});

// 请求拦截器 - 自动添加 Token
apiClient.interceptors.request.use(
  (config) => {
    const token = getToken();
    if (token) {
      config.headers.Authorization = `${API_CONFIG.AUTH.type} ${token}`;
    }
    return config;
  },
  (error) => {
    console.error("Request error:", error);
    return Promise.reject(error);
  }
);

// 响应拦截器 - 处理错误和 Token 失效
apiClient.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    if (error.response) {
      const { status, data } = error.response;

      // Token 失效或未授权
      if (status === 401) {
        console.error("认证失败 - Token 无效或已过期");
        clearToken();
        // TODO: 跳转到登录页
        // window.location.href = '/login';
      }

      // 权限不足
      if (status === 403) {
        console.error("权限不足");
      }

      // 服务器错误
      if (status >= 500) {
        console.error("服务器错误:", data?.message || "未知错误");
      }

      return Promise.reject(data || error.message);
    }

    // 网络错误
    if (error.request) {
      console.error("网络错误 - 无法连接到服务器");
      return Promise.reject(new Error("网络连接失败，请检查网络设置"));
    }

    return Promise.reject(error);
  }
);

/**
 * GET 请求
 * @param {string} url - 请求路径
 * @param {object} params - 查询参数
 * @returns {Promise}
 */
export const get = (url, params = {}) => {
  return apiClient.get(url, { params });
};

/**
 * POST 请求
 * @param {string} url - 请求路径
 * @param {object} data - 请求数据
 * @returns {Promise}
 */
export const post = (url, data = {}) => {
  return apiClient.post(url, data);
};

/**
 * PUT 请求
 * @param {string} url - 请求路径
 * @param {object} data - 请求数据
 * @returns {Promise}
 */
export const put = (url, data = {}) => {
  return apiClient.put(url, data);
};

/**
 * DELETE 请求
 * @param {string} url - 请求路径
 * @returns {Promise}
 */
export const del = (url) => {
  return apiClient.delete(url);
};

export default apiClient;
