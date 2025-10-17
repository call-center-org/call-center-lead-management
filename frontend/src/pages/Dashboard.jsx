import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";

const Dashboard = () => {
  const [packages, setPackages] = useState([]);
  const [metrics, setMetrics] = useState({
    totalPackages: 0,
    totalLeads: 0,
    avgContactRate: 0,
    avgInterestRate: 0,
  });

  // 后续将从 API 获取数据
  useEffect(() => {
    // TODO: 从 API 获取数据包列表和指标
    // fetchPackages();
    // fetchMetrics();
  }, []);

  return (
    <div className="space-y-6">
      {/* 关键指标卡片 */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white rounded-lg shadow-card p-card">
          <h3 className="text-sm text-gray-600 mb-2">数据包总数</h3>
          <p className="text-3xl font-bold text-primary">
            {metrics.totalPackages}
          </p>
        </div>
        <div className="bg-white rounded-lg shadow-card p-card">
          <h3 className="text-sm text-gray-600 mb-2">线索总量</h3>
          <p className="text-3xl font-bold text-secondary">
            {metrics.totalLeads}
          </p>
        </div>
        <div className="bg-white rounded-lg shadow-card p-card">
          <h3 className="text-sm text-gray-600 mb-2">平均接通率</h3>
          <p className="text-3xl font-bold text-success">
            {metrics.avgContactRate}%
          </p>
        </div>
        <div className="bg-white rounded-lg shadow-card p-card">
          <h3 className="text-sm text-gray-600 mb-2">平均意向率</h3>
          <p className="text-3xl font-bold text-warning">
            {metrics.avgInterestRate}%
          </p>
        </div>
      </div>

      {/* 数据包列表 */}
      <div className="bg-white rounded-lg shadow-card p-card">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold">数据包列表</h2>
          <Link
            to="/register"
            className="px-4 py-2 bg-primary text-white rounded-md hover:bg-blue-700 transition-colors"
          >
            + 登记新数据包
          </Link>
        </div>

        {packages.length === 0 ? (
          <div className="text-center py-12 text-gray-500">
            <p className="text-lg mb-2">暂无数据包</p>
            <p className="text-sm">点击上方按钮登记您的第一个数据包</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-3 text-left text-sm font-semibold text-gray-600">
                    数据包名称
                  </th>
                  <th className="px-4 py-3 text-left text-sm font-semibold text-gray-600">
                    来源
                  </th>
                  <th className="px-4 py-3 text-left text-sm font-semibold text-gray-600">
                    行业
                  </th>
                  <th className="px-4 py-3 text-left text-sm font-semibold text-gray-600">
                    线索数量
                  </th>
                  <th className="px-4 py-3 text-left text-sm font-semibold text-gray-600">
                    接通率
                  </th>
                  <th className="px-4 py-3 text-left text-sm font-semibold text-gray-600">
                    操作
                  </th>
                </tr>
              </thead>
              <tbody>
                {packages.map((pkg) => (
                  <tr key={pkg.id} className="border-t hover:bg-gray-50">
                    <td className="px-4 py-3">{pkg.name}</td>
                    <td className="px-4 py-3">{pkg.source}</td>
                    <td className="px-4 py-3">{pkg.industry}</td>
                    <td className="px-4 py-3">{pkg.totalLeads}</td>
                    <td className="px-4 py-3">{pkg.contactRate}%</td>
                    <td className="px-4 py-3">
                      <Link
                        to={`/package/${pkg.id}`}
                        className="text-primary hover:underline"
                      >
                        查看详情
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
