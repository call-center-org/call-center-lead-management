import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";

const PackageDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [packageData, setPackageData] = useState(null);
  const [dialTasks, setDialTasks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // TODO: 从 API 获取数据包详情
    // fetchPackageDetail(id);
    setLoading(false);
  }, [id]);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <p className="text-gray-500">加载中...</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* 返回按钮 */}
      <button
        onClick={() => navigate("/")}
        className="text-primary hover:underline flex items-center"
      >
        ← 返回数据包列表
      </button>

      {/* 数据包基本信息 */}
      <div className="bg-white rounded-lg shadow-card p-card">
        <h2 className="text-2xl font-semibold mb-4">数据包详情 #{id}</h2>

        {packageData ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <p className="text-sm text-gray-600">数据包名称</p>
              <p className="font-semibold">{packageData.name}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">数据来源</p>
              <p className="font-semibold">{packageData.source}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">行业类型</p>
              <p className="font-semibold">{packageData.industry}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">地区</p>
              <p className="font-semibold">{packageData.region}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">线索总量</p>
              <p className="font-semibold">{packageData.totalLeads}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">有效线索</p>
              <p className="font-semibold">{packageData.validLeads}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">接通率</p>
              <p className="font-semibold">{packageData.contactRate}%</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">意向率</p>
              <p className="font-semibold">{packageData.interestRate}%</p>
            </div>
          </div>
        ) : (
          <p className="text-gray-500">暂无数据</p>
        )}
      </div>

      {/* 外呼任务列表 */}
      <div className="bg-white rounded-lg shadow-card p-card">
        <h3 className="text-xl font-semibold mb-4">外呼任务</h3>

        {dialTasks.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            <p>暂无外呼任务</p>
          </div>
        ) : (
          <div className="space-y-4">
            {dialTasks.map((task) => (
              <div
                key={task.id}
                className="border rounded-lg p-4 hover:bg-gray-50"
              >
                <div className="flex justify-between items-start">
                  <div>
                    <h4 className="font-semibold">{task.taskName}</h4>
                    <p className="text-sm text-gray-600 mt-1">
                      开始时间: {new Date(task.startTime).toLocaleString()}
                    </p>
                    {task.endTime && (
                      <p className="text-sm text-gray-600">
                        结束时间: {new Date(task.endTime).toLocaleString()}
                      </p>
                    )}
                  </div>
                  <span
                    className={`px-3 py-1 rounded-full text-sm ${
                      task.status === "completed"
                        ? "bg-success text-white"
                        : task.status === "in_progress"
                        ? "bg-warning text-white"
                        : "bg-gray-300 text-gray-700"
                    }`}
                  >
                    {task.status === "completed"
                      ? "已完成"
                      : task.status === "in_progress"
                      ? "进行中"
                      : "待开始"}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* 标签统计 */}
      <div className="bg-white rounded-lg shadow-card p-card">
        <h3 className="text-xl font-semibold mb-4">标签统计</h3>
        <p className="text-gray-500">标签统计数据将在这里显示...</p>
      </div>
    </div>
  );
};

export default PackageDetail;
