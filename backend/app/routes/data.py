"""
数据统计相关 API 路由（为Widget MAC提供数据）
"""

from flask import Blueprint, jsonify
from datetime import date, datetime, timedelta
from app import db
from app.models import LeadPackage, DialTask, Call
from sqlalchemy import func

data_bp = Blueprint("data", __name__)


@data_bp.route("/remaining", methods=["GET"])
def get_data_remaining():
    """
    获取数据余量
    
    返回各年级的剩余线索数量
    """
    # 按年级统计剩余线索数量
    # 剩余数 = total_leads - (已外呼的条数)
    
    # 获取所有数据包的统计
    packages = LeadPackage.query.all()
    
    # 按年级分组统计
    by_level = {}
    total_remaining = 0
    
    for pkg in packages:
        industry = pkg.industry  # 年级字段
        
        # 计算该包的剩余数
        # 这里简化处理：剩余数 = valid_leads - sum(task.total_calls)
        total_calls = sum(task.total_calls for task in pkg.dial_tasks)
        remaining = max(0, pkg.valid_leads - total_calls)
        
        if industry not in by_level:
            by_level[industry] = 0
        
        by_level[industry] += remaining
        total_remaining += remaining
    
    # 判断是否数据余量偏低（小于1000条）
    is_low = total_remaining < 1000
    
    return jsonify({
        "success": True,
        "data": {
            "total_remaining": total_remaining,
            "by_level": by_level,
            "warning": {
                "is_low": is_low,
                "threshold": 1000,
                "message": "数据余量偏低，请及时采买" if is_low else None
            }
        }
    })


@data_bp.route("/consumption/month-total", methods=["GET"])
def get_month_consumption():
    """
    获取本月累计消耗
    
    消耗 = 已外呼的线索条数
    """
    # 获取本月第一天和最后一天
    today = date.today()
    first_day = date(today.year, today.month, 1)
    
    # 下个月第一天
    if today.month == 12:
        next_month = date(today.year + 1, 1, 1)
    else:
        next_month = date(today.year, today.month + 1, 1)
    
    # 统计本月所有外呼任务的total_calls
    month_tasks = DialTask.query.filter(
        DialTask.start_time >= first_day,
        DialTask.start_time < next_month
    ).all()
    
    # 按年级分组统计
    by_level = {}
    total_consumption = 0
    
    for task in month_tasks:
        # 获取任务对应的数据包
        package = task.package
        if package:
            industry = package.industry
            
            if industry not in by_level:
                by_level[industry] = 0
            
            by_level[industry] += task.total_calls
            total_consumption += task.total_calls
    
    # 计算日均消耗
    days_passed = (today - first_day).days + 1
    daily_average = total_consumption / days_passed if days_passed > 0 else 0
    
    # 预测月度总消耗
    days_in_month = (next_month - first_day).days
    projected_month_total = daily_average * days_in_month
    
    return jsonify({
        "success": True,
        "data": {
            "total_consumption": total_consumption,
            "by_level": by_level,
            "daily_average": round(daily_average, 2),
            "projected_month_total": round(projected_month_total, 0),
            "period": {
                "start_date": first_day.isoformat(),
                "end_date": today.isoformat(),
                "days_passed": days_passed,
                "days_in_month": days_in_month
            }
        }
    })


@data_bp.route("/value/package-progress", methods=["GET"])
def get_package_progress():
    """
    获取数据包进度
    
    返回所有活跃数据包的外呼进度
    """
    # 获取所有数据包
    packages = LeadPackage.query.order_by(LeadPackage.created_at.desc()).all()
    
    package_list = []
    total_progress = 0
    
    for pkg in packages:
        # 计算该包的进度
        total_calls = sum(task.total_calls for task in pkg.dial_tasks)
        progress_rate = (total_calls / pkg.valid_leads * 100) if pkg.valid_leads > 0 else 0
        
        package_list.append({
            "id": pkg.id,
            "name": pkg.name,
            "industry": pkg.industry,
            "total_leads": pkg.total_leads,
            "valid_leads": pkg.valid_leads,
            "called": total_calls,
            "remaining": max(0, pkg.valid_leads - total_calls),
            "progress_rate": round(progress_rate, 2),
            "contact_rate": round(pkg.contact_rate * 100, 2),
            "created_at": pkg.created_at.isoformat() if pkg.created_at else None
        })
        
        total_progress += progress_rate
    
    # 计算平均进度
    avg_progress = total_progress / len(packages) if packages else 0
    
    return jsonify({
        "success": True,
        "data": {
            "packages": package_list,
            "summary": {
                "total_packages": len(packages),
                "avg_progress": round(avg_progress, 2)
            }
        }
    })


@data_bp.route("/value/connect-rate", methods=["GET"])
def get_connect_rate():
    """
    获取接通率分析
    
    返回各维度的接通率统计
    """
    # 按年级统计接通率
    packages = LeadPackage.query.all()
    
    by_level = {}
    total_calls = 0
    total_connected = 0
    
    for pkg in packages:
        industry = pkg.industry
        
        # 统计该包的通话数据
        pkg_total_calls = sum(task.total_calls for task in pkg.dial_tasks)
        pkg_connected = sum(task.connected_calls for task in pkg.dial_tasks)
        
        if industry not in by_level:
            by_level[industry] = {
                "total_calls": 0,
                "connected_calls": 0,
                "contact_rate": 0
            }
        
        by_level[industry]["total_calls"] += pkg_total_calls
        by_level[industry]["connected_calls"] += pkg_connected
        
        total_calls += pkg_total_calls
        total_connected += pkg_connected
    
    # 计算各年级的接通率
    for industry in by_level:
        level_data = by_level[industry]
        if level_data["total_calls"] > 0:
            level_data["contact_rate"] = round(
                level_data["connected_calls"] / level_data["total_calls"] * 100, 2
            )
    
    # 总体接通率
    overall_rate = (total_connected / total_calls * 100) if total_calls > 0 else 0
    
    # 获取最近7天的趋势
    seven_days_ago = date.today() - timedelta(days=7)
    recent_tasks = DialTask.query.filter(
        DialTask.start_time >= seven_days_ago
    ).order_by(DialTask.start_time.asc()).all()
    
    # 按日期分组统计
    daily_stats = {}
    for task in recent_tasks:
        day = task.start_time.date().isoformat()
        if day not in daily_stats:
            daily_stats[day] = {"total_calls": 0, "connected_calls": 0}
        
        daily_stats[day]["total_calls"] += task.total_calls
        daily_stats[day]["connected_calls"] += task.connected_calls
    
    # 转换为趋势列表
    trend = []
    for day, stats in sorted(daily_stats.items()):
        rate = (stats["connected_calls"] / stats["total_calls"] * 100) if stats["total_calls"] > 0 else 0
        trend.append({
            "date": day,
            "contact_rate": round(rate, 2),
            "total_calls": stats["total_calls"],
            "connected_calls": stats["connected_calls"]
        })
    
    return jsonify({
        "success": True,
        "data": {
            "overall_rate": round(overall_rate, 2),
            "by_level": by_level,
            "total_calls": total_calls,
            "total_connected": total_connected,
            "trend_7days": trend
        }
    })


@data_bp.route("/purchase/week-plan", methods=["GET"])
def get_week_purchase_plan():
    """
    获取本周采买计划
    
    TODO: 需要添加采买计划相关的数据模型
    目前返回模拟数据
    """
    return jsonify({
        "success": True,
        "data": {
            "week": f"{date.today().isocalendar()[1]}周",
            "plans": [],
            "message": "采买计划功能开发中"
        }
    })

