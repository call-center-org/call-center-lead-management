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
          <div className="space-y-4">
            {(() => {
              // 按标签分类分组（基于标签代码前缀）
              const groupedTags = {
                '成功类': [],
                '可跟进类': [],
                '无效类': []
              };
              
              tagSummaries.forEach((summary) => {
                const tagCode = summary.tag_name;
                
                if (tagCode.startsWith('AS')) {
                  groupedTags['成功类'].push(summary);
                } else if (tagCode.startsWith('AF')) {
                  groupedTags['可跟进类'].push(summary);
                } else if (tagCode.startsWith('AN') || tagCode === 'AOT') {
                  groupedTags['无效类'].push(summary);
                }
              });

              // 颜色配置
              const colors = {
                '成功类': ['bg-green-600', 'bg-green-500', 'bg-green-400'],
                '可跟进类': ['bg-blue-600', 'bg-blue-500', 'bg-blue-400', 'bg-blue-300', 'bg-sky-500', 'bg-sky-400', 'bg-cyan-500', 'bg-cyan-400'],
                '无效类': ['bg-red-600', 'bg-red-500', 'bg-red-400', 'bg-orange-500', 'bg-orange-400']
              };

              return Object.entries(groupedTags).map(([categoryName, tags]) => {
                if (tags.length === 0) return null;
                
                // 计算该分类的总数
                const categoryTotal = tags.reduce((sum, tag) => sum + tag.tag_count, 0);
                const categoryColors = colors[categoryName];
                
                return (
                  <div key={categoryName}>
                    <div className="flex justify-between items-center mb-2">
                      <h4 className="font-medium text-sm text-gray-700">{categoryName}</h4>
                      <span className="text-sm text-gray-500">共 {formatNumber(categoryTotal)} 条</span>
                    </div>
                    
                    {/* 堆叠进度条 */}
                    <div className="relative w-full h-6 bg-gray-100 rounded-lg overflow-hidden flex">
                      {tags.map((tag, index) => {
                        const percentage = (tag.tag_count / categoryTotal) * 100;
                        const barColor = categoryColors[index % categoryColors.length];
                        
                        return (
                          <div
                            key={index}
                            className={`${barColor} h-full flex items-center justify-center transition-all hover:opacity-80 cursor-pointer group relative`}
                            style={{ width: `${percentage}%` }}
                            title={`${tag.tag_name} - ${tag.tag_value}: ${tag.tag_count} (${percentage.toFixed(1)}%)`}
                          >
                            {percentage > 8 && (
                              <span className="text-xs font-semibold text-white px-1 truncate">
                                {tag.tag_name}
                              </span>
                            )}
                            
                            {/* Tooltip on hover */}
                            <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 hidden group-hover:block z-10">
                              <div className="bg-gray-900 text-white text-xs rounded py-1 px-2 whitespace-nowrap">
                                {tag.tag_name} - {tag.tag_value}<br/>
                                {formatNumber(tag.tag_count)} ({percentage.toFixed(1)}%)
                              </div>
                              <div className="absolute top-full left-1/2 transform -translate-x-1/2 -mt-1">
                                <div className="border-4 border-transparent border-t-gray-900"></div>
                              </div>
                            </div>
                          </div>
                        );
                      })}
                    </div>
                    
                    {/* 标签图例 */}
                    <div className="mt-2 flex flex-wrap gap-x-4 gap-y-1">
                      {tags.map((tag, index) => {
                        const percentage = (tag.tag_count / categoryTotal) * 100;
                        const barColor = categoryColors[index % categoryColors.length];
                        
                        return (
                          <div key={index} className="flex items-center gap-1.5">
                            <div className={`w-3 h-3 rounded ${barColor}`}></div>
                            <span className="text-xs text-gray-600">
                              {tag.tag_name} 
                              <span className="text-gray-400 ml-1">
                                {formatNumber(tag.tag_count)} ({percentage.toFixed(1)}%)
                              </span>
                            </span>
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
