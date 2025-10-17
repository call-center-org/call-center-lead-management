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

      {/* 外呼任务列表 - 表格形式 */}
      <div className="bg-white rounded-lg shadow-card p-card">
        <h3 className="text-xl font-semibold mb-4">外呼任务</h3>

        {dialTasks.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            <p>暂无外呼任务</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-3 text-left font-semibold text-gray-600">任务日期</th>
                  <th className="px-4 py-3 text-left font-semibold text-gray-600">星期</th>
                  <th className="px-4 py-3 text-left font-semibold text-gray-600">任务ID</th>
                  <th className="px-4 py-3 text-left font-semibold text-gray-600">任务名</th>
                  <th className="px-4 py-3 text-right font-semibold text-gray-600">外呼数</th>
                  <th className="px-4 py-3 text-right font-semibold text-gray-600">剩余数</th>
                  <th className="px-4 py-3 text-right font-semibold text-gray-600">接通数</th>
                  <th className="px-4 py-3 text-right font-semibold text-gray-600">接通率</th>
                  <th className="px-4 py-3 text-right font-semibold text-gray-600">成功数</th>
                  <th className="px-4 py-3 text-right font-semibold text-gray-600">接通成功率</th>
                </tr>
              </thead>
              <tbody>
                {(() => {
                  // 按任务日期排序（最新的在上）
                  const sortedTasks = [...dialTasks].sort((a, b) => 
                    new Date(b.start_time) - new Date(a.start_time)
                  );
                  
                  // 计算累计外呼数（用于计算剩余数）
                  let cumulativeCalls = 0;
                  
                  return sortedTasks.map((task, index) => {
                    cumulativeCalls += task.total_calls || 0;
                    
                    const taskDate = task.start_time ? new Date(task.start_time) : null;
                    const dateStr = taskDate ? taskDate.toLocaleDateString('zh-CN') : '-';
                    const weekDay = taskDate ? ['日', '一', '二', '三', '四', '五', '六'][taskDate.getDay()] : '-';
                    
                    // 剩余数 = 总线索数 - 累计外呼数
                    const remaining = packageData ? packageData.total_leads - cumulativeCalls : 0;
                    
                    // 接通率 = 接通数 / 外呼数
                    const contactRate = task.total_calls > 0 
                      ? ((task.connected_calls || 0) / task.total_calls * 100).toFixed(2) 
                      : '0.00';
                    
                    // 接通成功率 = 成功数 / 接通数
                    const successRate = (task.connected_calls || 0) > 0
                      ? ((task.interested_calls || 0) / task.connected_calls * 100).toFixed(2)
                      : '0.00';
                    
                    return (
                      <tr key={task.id} className="border-t hover:bg-gray-50">
                        <td className="px-4 py-3">{dateStr}</td>
                        <td className="px-4 py-3">周{weekDay}</td>
                        <td className="px-4 py-3 text-gray-600">{task.id}</td>
                        <td className="px-4 py-3 font-medium">{task.task_name}</td>
                        <td className="px-4 py-3 text-right font-mono">{formatNumber(task.total_calls || 0)}</td>
                        <td className="px-4 py-3 text-right font-mono text-blue-600">{formatNumber(remaining)}</td>
                        <td className="px-4 py-3 text-right font-mono text-success">{formatNumber(task.connected_calls || 0)}</td>
                        <td className="px-4 py-3 text-right font-mono">{contactRate}%</td>
                        <td className="px-4 py-3 text-right font-mono text-warning">{formatNumber(task.interested_calls || 0)}</td>
                        <td className="px-4 py-3 text-right font-mono">{successRate}%</td>
                      </tr>
                    );
                  });
                })()}
              </tbody>
              {/* 表格汇总行 */}
              <tfoot className="bg-gray-50 border-t-2">
                <tr>
                  <td colSpan="4" className="px-4 py-3 text-right font-semibold">汇总：</td>
                  <td className="px-4 py-3 text-right font-bold font-mono">
                    {formatNumber(dialTasks.reduce((sum, t) => sum + (t.total_calls || 0), 0))}
                  </td>
                  <td className="px-4 py-3 text-right font-bold font-mono text-blue-600">
                    {packageData ? formatNumber(packageData.total_leads - dialTasks.reduce((sum, t) => sum + (t.total_calls || 0), 0)) : '-'}
                  </td>
                  <td className="px-4 py-3 text-right font-bold font-mono text-success">
                    {formatNumber(dialTasks.reduce((sum, t) => sum + (t.connected_calls || 0), 0))}
                  </td>
                  <td className="px-4 py-3 text-right font-bold font-mono">
                    {(() => {
                      const totalCalls = dialTasks.reduce((sum, t) => sum + (t.total_calls || 0), 0);
                      const totalConnected = dialTasks.reduce((sum, t) => sum + (t.connected_calls || 0), 0);
                      return totalCalls > 0 ? ((totalConnected / totalCalls * 100).toFixed(2)) : '0.00';
                    })()}%
                  </td>
                  <td className="px-4 py-3 text-right font-bold font-mono text-warning">
                    {formatNumber(dialTasks.reduce((sum, t) => sum + (t.interested_calls || 0), 0))}
                  </td>
                  <td className="px-4 py-3 text-right font-bold font-mono">
                    {(() => {
                      const totalConnected = dialTasks.reduce((sum, t) => sum + (t.connected_calls || 0), 0);
                      const totalInterested = dialTasks.reduce((sum, t) => sum + (t.interested_calls || 0), 0);
                      return totalConnected > 0 ? ((totalInterested / totalConnected * 100).toFixed(2)) : '0.00';
                    })()}%
                  </td>
                </tr>
              </tfoot>
            </table>
          </div>
        )}
      </div>

      {/* 标签统计 */}
      <div className="bg-white rounded-lg shadow-card p-4">
        <h3 className="text-lg font-semibold mb-3">标签统计</h3>
        
        {tagSummaries.length === 0 ? (
          <p className="text-gray-500 text-center py-4 text-sm">暂无标签统计数据</p>
        ) : (
          <div className="space-y-3">
            {(() => {
              // 按标签分类分组（基于标签代码前缀）
              const groupedTags = {
                '成功类': [],
                '可跟进类': [],
                '无效类': [],
                '其他': []
              };
              
              tagSummaries.forEach((summary) => {
                const tagCode = summary.tag_name; // AS1, AF2 等
                
                if (tagCode.startsWith('AS')) {
                  groupedTags['成功类'].push(summary);
                } else if (tagCode.startsWith('AF')) {
                  groupedTags['可跟进类'].push(summary);
                } else if (tagCode.startsWith('AN') || tagCode === 'AOT') {
                  groupedTags['无效类'].push(summary);
                } else {
                  groupedTags['其他'].push(summary);
                }
              });

              return Object.entries(groupedTags).map(([categoryName, tags]) => {
                if (tags.length === 0) return null;
                
                return (
                  <div key={categoryName} className="border rounded p-2">
                    <h4 className="font-medium text-sm mb-2 text-gray-700">{categoryName}</h4>
                    
                    <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-2">
                      {tags.map((tag, index) => {
                        const percentage = (tag.percentage * 100).toFixed(1);
                        
                        // 根据标签分类选择颜色
                        let bgColor = 'bg-gray-50';
                        let textColor = 'text-gray-600';
                        let barColor = 'bg-gray-400';
                        
                        if (categoryName === '成功类') {
                          bgColor = 'bg-green-50';
                          textColor = 'text-green-600';
                          barColor = 'bg-green-500';
                        } else if (categoryName === '可跟进类') {
                          bgColor = 'bg-blue-50';
                          textColor = 'text-blue-600';
                          barColor = 'bg-blue-500';
                        } else if (categoryName === '无效类') {
                          bgColor = 'bg-red-50';
                          textColor = 'text-red-600';
                          barColor = 'bg-red-500';
                        }
                        
                        return (
                          <div key={index} className={`${bgColor} rounded p-2`}>
                            <div className="flex justify-between items-center mb-1">
                              <span className={`text-xs font-bold ${textColor}`}>
                                {tag.tag_name}
                              </span>
                              <span className="text-xs font-mono font-semibold text-gray-600">
                                {formatNumber(tag.tag_count)}
                              </span>
                            </div>
                            
                            <div className={`text-xs ${textColor} mb-1 truncate`} title={tag.tag_value}>
                              {tag.tag_value}
                            </div>
                            
                            {/* 进度条 */}
                            <div className="relative w-full h-1 bg-white rounded-full overflow-hidden">
                              <div
                                className={`h-full ${barColor} rounded-full transition-all`}
                                style={{ width: `${percentage}%` }}
                              ></div>
                            </div>
                            
                            <div className="mt-0.5 text-right">
                              <span className="text-xs text-gray-500">
                                {percentage}%
                              </span>
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                );
              }).filter(Boolean);
            })()}
          </div>
        )}
      </div>
    </div>
  );
};

export default PackageDetail;
