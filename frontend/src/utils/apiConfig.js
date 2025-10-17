// 根据环境动态设置 API 基础路径
const getBaseURL = () => {
  // 开发环境
  if (import.meta.env.MODE === "development") {
    return "http://localhost:5002/api";
  }
  
  // 生产环境 - 检测不同的部署平台
  const hostname = window.location.hostname;
  
  // CloudBase 环境
  if (hostname.includes("tcloudbase.com")) {
    return "/lead-api";
  }
  
  // Zeabur 环境 - 使用环境变量或默认后端域名
  if (hostname.includes("zeabur.app")) {
    // Zeabur 会自动注入后端服务的域名作为环境变量
    return import.meta.env.VITE_API_URL || "https://backend.zeabur.app/api";
  }
  
  // 默认使用相对路径
  return "/api";
};

export const API_CONFIG = {
  BASE_URL: getBaseURL(),
  AUTH: {
    type: "Bearer",
  },
  ENDPOINTS: {
    // 数据包相关
    getPackages: "/packages",
    createPackage: "/packages",
    getPackage: "/packages/:id",
    updatePackage: "/packages/:id",
    deletePackage: "/packages/:id",

    // 外呼任务相关
    createDialTask: "/packages/:id/tasks",
    getDialTasks: "/packages/:id/tasks",

    // 通话记录相关
    getCalls: "/tasks/:id/calls",
    createCall: "/tasks/:id/calls",

    // 标签相关
    getPackageTags: "/packages/:id/tags",

    // 指标相关
    getMetrics: "/metrics",
    getDashboard: "/dashboard",
  },
  TIMEOUT: 30000,
};

export default API_CONFIG;
