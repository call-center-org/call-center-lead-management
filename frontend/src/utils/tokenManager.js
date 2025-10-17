// Token 管理工具
// 用于管理 JWT Token 的存储、获取和清除

const TOKEN_KEY = "authToken";
const TOKEN_EXPIRY_KEY = "authTokenExpiry";

/**
 * 获取存储的 Token
 * @returns {string} Token 字符串，如果不存在或已过期则返回空字符串
 */
export const getToken = () => {
  const token = localStorage.getItem(TOKEN_KEY);
  const expiry = localStorage.getItem(TOKEN_EXPIRY_KEY);

  // 检查 Token 是否过期
  if (expiry && new Date().getTime() > parseInt(expiry)) {
    clearToken();
    return "";
  }

  return token || "";
};

/**
 * 存储 Token
 * @param {string} token - JWT Token
 * @param {number} expiresIn - Token 有效期（秒）
 */
export const setToken = (token, expiresIn = 86400) => {
  localStorage.setItem(TOKEN_KEY, token);

  // 设置过期时间（当前时间 + 有效期）
  const expiryTime = new Date().getTime() + expiresIn * 1000;
  localStorage.setItem(TOKEN_EXPIRY_KEY, expiryTime.toString());
};

/**
 * 清除 Token
 */
export const clearToken = () => {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(TOKEN_EXPIRY_KEY);
};

/**
 * 检查 Token 是否存在且有效
 * @returns {boolean}
 */
export const isAuthenticated = () => {
  return getToken() !== "";
};

export default {
  getToken,
  setToken,
  clearToken,
  isAuthenticated,
};
