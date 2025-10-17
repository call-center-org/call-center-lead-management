import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import toast from "react-hot-toast";
import apiClient from "../utils/apiClient";

const PackageRegister = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: "",
    companyCode: "107848", // 指定公司
    source: "采买", // 包属性：采买/练习
    industry: "高中", // 年级
    totalLeads: "",
    validLeads: "",
    costPerLead: "", // 单条成本（可选）
  });

  // 自动识别的字段
  const [autoFields, setAutoFields] = useState({
    region: "", // 对应职场
    releaseDate: "", // 下放日期
    attributeValue: "", // 属性值
    internalCode: "", // 内部代号
    taskPrefix: "", // 内部初次任务前缀
  });

  // 公司代码映射
  const companyCodeMap = {
    "107847": "禹州",
    "107849": "宜宾",
    "107848": "淮安",
  };

  // 自动识别函数
  useEffect(() => {
    // 1. 识别对应职场
    const region = companyCodeMap[formData.companyCode] || "";

    // 2. 从数据包名称提取下放日期（8位日期的后4位）
    let releaseDate = "";
    const dateMatch = formData.name.match(/(\d{8})/);
    if (dateMatch) {
      const fullDate = dateMatch[1]; // 如：20250826
      releaseDate = fullDate.slice(4); // 取后4位：0826
    }

    // 3. 根据包属性自动填写属性值
    // 采买 → N，练习 → P1
    const attributeValue = formData.source === "采买" ? "N" : "P1";

    // 4. 生成内部代号：{职场}-{日期}-{年级}-{有效数}
    const internalCode =
      region && releaseDate && formData.industry && formData.validLeads
        ? `${region}-${releaseDate}-${formData.industry}-${formData.validLeads}`
        : "";

    // 5. 生成内部初次任务前缀：{内部代号}-{属性值}
    const taskPrefix = internalCode ? `${internalCode}-${attributeValue}` : "";

    setAutoFields({
      region,
      releaseDate,
      attributeValue,
      internalCode,
      taskPrefix,
    });
  }, [
    formData.name,
    formData.companyCode,
    formData.source,
    formData.industry,
    formData.validLeads,
  ]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => {
      const newData = { ...prev, [name]: value };
      
      // 如果总数改变且有效数为空，自动设置有效数等于总数
      if (name === "totalLeads" && !prev.validLeads) {
        newData.validLeads = value;
      }
      
      return newData;
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      // 构建API请求数据
      const requestData = {
        name: formData.name,
        source: formData.source,
        industry: formData.industry,
        region: autoFields.region,
        total_leads: parseInt(formData.totalLeads),
        valid_leads: parseInt(formData.validLeads || formData.totalLeads),
        cost_per_lead: parseFloat(formData.costPerLead || 0),
      };

      await apiClient.post("/packages", requestData);

      toast.success("数据包登记成功！");
      navigate("/");
    } catch (error) {
      toast.error("登记失败，请重试");
      console.error("Error creating package:", error);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-card p-card">
        <div className="mb-6">
          <h2 className="text-2xl font-semibold">数据包登记表</h2>
          <p className="text-sm text-gray-500 mt-1">
            🔴 红色标记为手动输入 | 🟢 绿色标记为自动识别
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* 手动输入字段 */}
          <div className="space-y-4 border-l-4 border-red-400 pl-4">
            <h3 className="text-lg font-semibold text-gray-700 flex items-center">
              <span className="inline-block w-3 h-3 bg-red-400 rounded-full mr-2"></span>
              手动输入字段
            </h3>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                数据包名称 <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleChange}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
                placeholder="例如：dyac1-20250826-高中加购.csv"
              />
              <p className="text-xs text-gray-500 mt-1">
                💡 请包含8位日期（如：20250826），系统将自动提取下放日期
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  指定公司 <span className="text-red-500">*</span>
                </label>
                <select
                  name="companyCode"
                  value={formData.companyCode}
                  onChange={handleChange}
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
                >
                  <option value="107848">107848 - 淮安</option>
                  <option value="107847">107847 - 禹州</option>
                  <option value="107849">107849 - 宜宾</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  年级 <span className="text-red-500">*</span>
                </label>
                <select
                  name="industry"
                  value={formData.industry}
                  onChange={handleChange}
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
                >
                  <option value="高中">高中</option>
                  <option value="初中">初中</option>
                  <option value="小学">小学</option>
                  <option value="幼儿">幼儿</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  包属性 <span className="text-red-500">*</span>
                </label>
                <select
                  name="source"
                  value={formData.source}
                  onChange={handleChange}
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
                >
                  <option value="采买">采买</option>
                  <option value="练习">练习</option>
                </select>
                <p className="text-xs text-gray-500 mt-1">
                  采买→N | 练习→P1
                </p>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  总数 <span className="text-red-500">*</span>
                </label>
                <input
                  type="number"
                  name="totalLeads"
                  value={formData.totalLeads}
                  onChange={handleChange}
                  required
                  min="0"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
                  placeholder="例如：5000"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  有效数 <span className="text-red-500">*</span>
                </label>
                <input
                  type="number"
                  name="validLeads"
                  value={formData.validLeads}
                  onChange={handleChange}
                  required
                  min="0"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
                  placeholder="例如：5000"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  单条成本（元）
                </label>
                <input
                  type="number"
                  name="costPerLead"
                  value={formData.costPerLead}
                  onChange={handleChange}
                  min="0"
                  step="0.01"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
                  placeholder="选填"
                />
              </div>
            </div>
          </div>

          {/* 自动识别字段预览 */}
          <div className="space-y-4 border-l-4 border-green-400 pl-4">
            <h3 className="text-lg font-semibold text-gray-700 flex items-center">
              <span className="inline-block w-3 h-3 bg-green-400 rounded-full mr-2"></span>
              自动识别字段（预览）
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <div className="bg-green-50 p-3 rounded-md">
                <div className="text-xs text-gray-600 mb-1">对应职场</div>
                <div className="text-lg font-semibold text-green-700">
                  {autoFields.region || "-"}
                </div>
                <div className="text-xs text-gray-500 mt-1">
                  根据指定公司自动识别
                </div>
              </div>

              <div className="bg-green-50 p-3 rounded-md">
                <div className="text-xs text-gray-600 mb-1">下放日期</div>
                <div className="text-lg font-semibold text-green-700">
                  {autoFields.releaseDate || "-"}
                </div>
                <div className="text-xs text-gray-500 mt-1">
                  从数据包名称提取
                </div>
              </div>

              <div className="bg-green-50 p-3 rounded-md">
                <div className="text-xs text-gray-600 mb-1">属性值</div>
                <div className="text-lg font-semibold text-green-700">
                  {autoFields.attributeValue || "-"}
                </div>
                <div className="text-xs text-gray-500 mt-1">
                  采买→N | 练习→P1
                </div>
              </div>

              <div className="bg-green-50 p-3 rounded-md col-span-full lg:col-span-2">
                <div className="text-xs text-gray-600 mb-1">内部代号</div>
                <div className="text-lg font-semibold text-green-700 font-mono">
                  {autoFields.internalCode || "等待数据完善..."}
                </div>
                <div className="text-xs text-gray-500 mt-1">
                  格式：职场-日期-年级-有效数
                </div>
              </div>

              <div className="bg-green-50 p-3 rounded-md border-2 border-green-400 col-span-full">
                <div className="text-xs text-gray-600 mb-1 flex items-center">
                  <span className="inline-block w-2 h-2 bg-green-500 rounded-full mr-1"></span>
                  内部初次任务前缀
                </div>
                <div className="text-xl font-bold text-green-700 font-mono">
                  {autoFields.taskPrefix || "等待数据完善..."}
                </div>
                <div className="text-xs text-gray-500 mt-1">
                  格式：职场-日期-年级-有效数-属性值
                </div>
              </div>
            </div>
          </div>

          {/* 成本预估 */}
          {formData.totalLeads && formData.costPerLead && (
            <div className="bg-blue-50 border border-blue-200 rounded-md p-4">
              <div className="flex justify-between items-center">
                <span className="text-sm font-medium text-gray-700">
                  总成本预估
                </span>
                <span className="text-2xl font-bold text-primary">
                  ¥
                  {(
                    parseFloat(formData.totalLeads) *
                    parseFloat(formData.costPerLead)
                  ).toFixed(2)}
                </span>
              </div>
            </div>
          )}

          {/* 提交按钮 */}
          <div className="flex justify-end space-x-4 pt-4 border-t">
            <button
              type="button"
              onClick={() => navigate("/")}
              className="px-6 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 transition-colors"
            >
              取消
            </button>
            <button
              type="submit"
              disabled={!autoFields.taskPrefix}
              className="px-6 py-2 bg-primary text-white rounded-md hover:bg-blue-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
            >
              {autoFields.taskPrefix ? "提交登记" : "请完善必填字段"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default PackageRegister;
