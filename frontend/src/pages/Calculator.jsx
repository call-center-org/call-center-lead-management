import React, { useState } from "react";

const Calculator = () => {
  const [inputs, setInputs] = useState({
    targetLeads: "",
    contactRate: "",
    interestRate: "",
    costPerLead: "",
    revenuePerLead: "",
  });

  const [results, setResults] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setInputs((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const calculate = () => {
    const {
      targetLeads,
      contactRate,
      interestRate,
      costPerLead,
      revenuePerLead,
    } = inputs;

    // 验证输入
    if (!targetLeads || !contactRate || !interestRate) {
      alert("请填写必填项");
      return;
    }

    const target = parseFloat(targetLeads);
    const contact = parseFloat(contactRate) / 100;
    const interest = parseFloat(interestRate) / 100;
    const cost = parseFloat(costPerLead) || 0;
    const revenue = parseFloat(revenuePerLead) || 0;

    // 计算所需线索量
    const requiredLeads = Math.ceil(target / (contact * interest));

    // 计算预期接通量
    const expectedContacts = Math.round(requiredLeads * contact);

    // 计算预期意向量
    const expectedInterested = Math.round(expectedContacts * interest);

    // 计算成本和收益
    const totalCost = requiredLeads * cost;
    const totalRevenue = expectedInterested * revenue;
    const profit = totalRevenue - totalCost;
    const roi = totalCost > 0 ? ((profit / totalCost) * 100).toFixed(2) : 0;

    setResults({
      requiredLeads,
      expectedContacts,
      expectedInterested,
      totalCost,
      totalRevenue,
      profit,
      roi,
    });
  };

  const reset = () => {
    setInputs({
      targetLeads: "",
      contactRate: "",
      interestRate: "",
      costPerLead: "",
      revenuePerLead: "",
    });
    setResults(null);
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-card p-card">
        <h2 className="text-2xl font-semibold mb-6">线索需求计算器</h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* 输入区域 */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-gray-700 border-b pb-2">
              输入参数
            </h3>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                目标意向客户数 <span className="text-red-500">*</span>
              </label>
              <input
                type="number"
                name="targetLeads"
                value={inputs.targetLeads}
                onChange={handleChange}
                min="0"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
                placeholder="例如：100"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                预期接通率 (%) <span className="text-red-500">*</span>
              </label>
              <input
                type="number"
                name="contactRate"
                value={inputs.contactRate}
                onChange={handleChange}
                min="0"
                max="100"
                step="0.1"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
                placeholder="例如：35"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                预期意向率 (%) <span className="text-red-500">*</span>
              </label>
              <input
                type="number"
                name="interestRate"
                value={inputs.interestRate}
                onChange={handleChange}
                min="0"
                max="100"
                step="0.1"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
                placeholder="例如：15"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                单条线索成本 (元)
              </label>
              <input
                type="number"
                name="costPerLead"
                value={inputs.costPerLead}
                onChange={handleChange}
                min="0"
                step="0.01"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
                placeholder="例如：5"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                单个意向客户收益 (元)
              </label>
              <input
                type="number"
                name="revenuePerLead"
                value={inputs.revenuePerLead}
                onChange={handleChange}
                min="0"
                step="0.01"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
                placeholder="例如：50"
              />
            </div>

            <div className="flex space-x-4 pt-4">
              <button
                onClick={calculate}
                className="flex-1 px-4 py-2 bg-primary text-white rounded-md hover:bg-blue-700 transition-colors"
              >
                计算
              </button>
              <button
                onClick={reset}
                className="px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 transition-colors"
              >
                重置
              </button>
            </div>
          </div>

          {/* 结果区域 */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-gray-700 border-b pb-2">
              计算结果
            </h3>

            {results ? (
              <div className="space-y-4">
                <div className="bg-blue-50 border-l-4 border-primary p-4 rounded">
                  <p className="text-sm text-gray-600">所需线索总量</p>
                  <p className="text-3xl font-bold text-primary">
                    {results.requiredLeads}
                  </p>
                </div>

                <div className="bg-green-50 border-l-4 border-success p-4 rounded">
                  <p className="text-sm text-gray-600">预期接通量</p>
                  <p className="text-2xl font-bold text-success">
                    {results.expectedContacts}
                  </p>
                </div>

                <div className="bg-purple-50 border-l-4 border-secondary p-4 rounded">
                  <p className="text-sm text-gray-600">预期意向量</p>
                  <p className="text-2xl font-bold text-secondary">
                    {results.expectedInterested}
                  </p>
                </div>

                {inputs.costPerLead && (
                  <div className="bg-orange-50 border-l-4 border-warning p-4 rounded">
                    <p className="text-sm text-gray-600">总成本</p>
                    <p className="text-2xl font-bold text-warning">
                      ¥{results.totalCost.toFixed(2)}
                    </p>
                  </div>
                )}

                {inputs.revenuePerLead && (
                  <>
                    <div className="bg-green-50 border-l-4 border-success p-4 rounded">
                      <p className="text-sm text-gray-600">预期收益</p>
                      <p className="text-2xl font-bold text-success">
                        ¥{results.totalRevenue.toFixed(2)}
                      </p>
                    </div>

                    <div
                      className={`border-l-4 p-4 rounded ${
                        results.profit >= 0
                          ? "bg-green-50 border-success"
                          : "bg-red-50 border-danger"
                      }`}
                    >
                      <p className="text-sm text-gray-600">净利润</p>
                      <p
                        className={`text-2xl font-bold ${
                          results.profit >= 0 ? "text-success" : "text-danger"
                        }`}
                      >
                        ¥{results.profit.toFixed(2)}
                      </p>
                    </div>

                    {inputs.costPerLead && (
                      <div className="bg-blue-50 border-l-4 border-primary p-4 rounded">
                        <p className="text-sm text-gray-600">
                          投资回报率 (ROI)
                        </p>
                        <p className="text-2xl font-bold text-primary">
                          {results.roi}%
                        </p>
                      </div>
                    )}
                  </>
                )}
              </div>
            ) : (
              <div className="text-center py-12 text-gray-500">
                <p>请填写左侧参数并点击「计算」按钮</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Calculator;
