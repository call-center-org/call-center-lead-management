/**
 * 数字格式化工具
 */

/**
 * 格式化数字，添加千位符
 * @param {number|string} num - 要格式化的数字
 * @param {number} decimals - 小数位数，默认0
 * @returns {string} 格式化后的字符串
 */
export const formatNumber = (num, decimals = 0) => {
  if (num === null || num === undefined || num === '') return '-';
  
  const number = parseFloat(num);
  if (isNaN(number)) return '-';
  
  return number.toLocaleString('zh-CN', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  });
};

/**
 * 格式化百分比
 * @param {number} num - 0-1之间的小数或0-100的数字
 * @param {number} decimals - 小数位数，默认2
 * @param {boolean} isDecimal - 是否是0-1之间的小数，默认true
 * @returns {string} 格式化后的百分比字符串
 */
export const formatPercent = (num, decimals = 2, isDecimal = true) => {
  if (num === null || num === undefined || num === '') return '-';
  
  const number = parseFloat(num);
  if (isNaN(number)) return '-';
  
  const percent = isDecimal ? number * 100 : number;
  return `${percent.toFixed(decimals)}%`;
};

/**
 * 格式化金额
 * @param {number} num - 金额数字
 * @param {number} decimals - 小数位数，默认2
 * @returns {string} 格式化后的金额字符串
 */
export const formatCurrency = (num, decimals = 2) => {
  if (num === null || num === undefined || num === '') return '¥0.00';
  
  const number = parseFloat(num);
  if (isNaN(number)) return '¥0.00';
  
  return `¥${number.toLocaleString('zh-CN', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  })}`;
};

/**
 * 格式化大数字（K, M, B）
 * @param {number} num - 数字
 * @returns {string} 格式化后的字符串
 */
export const formatLargeNumber = (num) => {
  if (num === null || num === undefined || num === '') return '-';
  
  const number = parseFloat(num);
  if (isNaN(number)) return '-';
  
  if (number >= 1000000000) {
    return `${(number / 1000000000).toFixed(1)}B`;
  }
  if (number >= 1000000) {
    return `${(number / 1000000).toFixed(1)}M`;
  }
  if (number >= 1000) {
    return `${(number / 1000).toFixed(1)}K`;
  }
  return number.toString();
};

