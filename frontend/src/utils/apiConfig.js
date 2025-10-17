export const API_CONFIG = {
  BASE_URL: "/api", // 代理到后端
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
