import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import apiClient from "../utils/apiClient";
import { formatNumber, formatPercent, formatCurrency } from "../utils/formatNumber";
import toast from "react-hot-toast";

const PackageDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [packageData, setPackageData] = useState(null);
  const [dialTasks, setDialTasks] = useState([]);
  const [tagSummaries, setTagSummaries] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchPackageDetail();
  }, [id]);

  const fetchPackageDetail = async () => {
    try {
      setLoading(true);
      
      // 获取数据包详情
      const response = await apiClient.get(`/packages/${id}`);
      
      if (response.success) {
        const data = response.data;
        setPackageData(data);
        setDialTasks(data.dial_tasks || []);
        setTagSummaries(data.tag_summaries || []);
      }
    } catch (error) {
      console.error("Failed to fetch package detail:", error);
      toast.error("加载数据失败");
    } finally {
      setLoading(false);
    }
  };

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
        <h2 className="text-2xl font-semibold mb-4">数据包详情</h2>

        {packageData ? (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="md:col-span-3 border-b pb-4">
              <p className="text-sm text-gray-600">数据包名称</p>
              <p className="text-lg font-semibold">{packageData.name}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">包属性</p>
              <p className="font-semibold">{packageData.source || "-"}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">对应职场</p>
              <p className="font-semibold">{packageData.region || "-"}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">年级</p>
              <p className="font-semibold">{packageData.industry || "-"}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">总数</p>
              <p className="font-semibold font-mono">{formatNumber(packageData.total_leads)}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">有效数</p>
              <p className="font-semibold font-mono">{formatNumber(packageData.valid_leads)}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">单条成本</p>
              <p className="font-semibold font-mono">{formatCurrency(packageData.cost_per_lead)}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">总成本</p>
              <p className="font-semibold font-mono text-lg text-primary">
                {formatCurrency(packageData.total_cost)}
              </p>
            </div>
            <div>
              <p className="text-sm text-gray-600">接通率</p>
              <p className="font-semibold text-success">{formatPercent(packageData.contact_rate)}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">意向率</p>
              <p className="font-semibold text-warning">{formatPercent(packageData.interest_rate)}</p>
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
                className="border rounded-lg p-4 hover:bg-gray-50 transition-colors"
              >
                <div className="flex justify-between items-start mb-3">
                  <div>
                    <h4 className="font-semibold text-lg">{task.task_name}</h4>
                    {task.description && (
                      <p className="text-sm text-gray-600 mt-1">{task.description}</p>
                    )}
                  </div>
                  <span
                    className={`px-3 py-1 rounded-full text-sm font-medium ${
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

                {/* 任务时间 */}
                <div className="grid grid-cols-2 gap-4 mb-3 text-sm">
                  <div>
                    <span className="text-gray-600">开始时间: </span>
                    <span className="font-medium">
                      {task.start_time ? new Date(task.start_time).toLocaleString('zh-CN') : "-"}
                    </span>
                  </div>
                  {task.end_time && (
                    <div>
                      <span className="text-gray-600">结束时间: </span>
                      <span className="font-medium">
                        {new Date(task.end_time).toLocaleString('zh-CN')}
                      </span>
                    </div>
                  )}
                </div>

                {/* 任务统计 */}
                <div className="grid grid-cols-3 gap-4 pt-3 border-t">
                  <div className="text-center">
                    <p className="text-sm text-gray-600">总呼叫</p>
                    <p className="text-lg font-bold text-primary">
                      {formatNumber(task.total_calls || 0)}
                    </p>
                  </div>
                  <div className="text-center">
                    <p className="text-sm text-gray-600">接通数</p>
                    <p className="text-lg font-bold text-success">
                      {formatNumber(task.connected_calls || 0)}
                    </p>
                  </div>
                  <div className="text-center">
                    <p className="text-sm text-gray-600">意向数</p>
                    <p className="text-lg font-bold text-warning">
                      {formatNumber(task.interested_calls || 0)}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* 标签统计 */}
      <div className="bg-white rounded-lg shadow-card p-card">
        <h3 className="text-xl font-semibold mb-4">标签统计</h3>
        
        {tagSummaries.length === 0 ? (
          <p className="text-gray-500 text-center py-8">暂无标签统计数据</p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {tagSummaries.map((summary, index) => (
              <div key={index} className="border rounded-lg p-4">
                <p className="text-sm text-gray-600">{summary.tag_name}</p>
                <p className="text-2xl font-bold text-primary mt-2">
                  {formatNumber(summary.tag_count || 0)}
                </p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default PackageDetail;
