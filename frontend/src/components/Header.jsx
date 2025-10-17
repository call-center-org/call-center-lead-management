import React from "react";
import { NavLink } from "react-router-dom";

const Header = ({ activeTab, setActiveTab }) => {
  const tabs = [
    { id: "dashboard", label: "首页看板", path: "/" },
    { id: "register", label: "数据包登记", path: "/register" },
    { id: "calculator", label: "需求计算器", path: "/calculator" },
  ];

  return (
    <header className="bg-white shadow-md">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center py-4">
          <h1 className="text-2xl font-bold text-primary">
            线索数据包管理系统
          </h1>

          <nav className="flex space-x-1">
            {tabs.map((tab) => (
              <NavLink
                key={tab.id}
                to={tab.path}
                className={({ isActive }) =>
                  `px-4 py-2 rounded-md transition-colors ${
                    isActive
                      ? "bg-primary text-white"
                      : "text-gray-600 hover:bg-gray-100"
                  }`
                }
                onClick={() => setActiveTab(tab.id)}
              >
                {tab.label}
              </NavLink>
            ))}
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header;
