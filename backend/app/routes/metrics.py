"""
指标查询相关 API 路由
"""
from flask import Blueprint, request, jsonify
from datetime import date, datetime, timedelta
from app import db
from app.models import LeadPackage, DialTask, Call, MetricsSummary

metrics_bp = Blueprint('metrics', __name__)


@metrics_bp.route('/dashboard', methods=['GET'])
def get_dashboard_metrics():
    """
    获取仪表盘数据
    
    返回:
        - 关键指标卡片数据
        - 最近的数据包列表
        - 今日统计
    """
    # 统计数据包
    total_packages = LeadPackage.query.count()
    total_leads = db.session.query(
        db.func.sum(LeadPackage.total_leads)
    ).scalar() or 0
    
    # 计算平均接通率和意向率
    avg_contact_rate = db.session.query(
        db.func.avg(LeadPackage.contact_rate)
    ).scalar() or 0.0
    
    avg_interest_rate = db.session.query(
        db.func.avg(LeadPackage.interest_rate)
    ).scalar() or 0.0
    
    # 今日通话统计
    today = date.today()
    today_calls = Call.query.filter(
        db.func.date(Call.call_time) == today
    ).count()
    
    today_connected = Call.query.filter(
        db.func.date(Call.call_time) == today,
        Call.result == 'connected'
    ).count()
    
    # 最近的数据包（前10个）
    recent_packages = LeadPackage.query.order_by(
        LeadPackage.created_at.desc()
    ).limit(10).all()
    
    return jsonify({
        'success': True,
        'data': {
            'summary': {
                'total_packages': total_packages,
                'total_leads': total_leads,
                'avg_contact_rate': round(avg_contact_rate, 4),
                'avg_interest_rate': round(avg_interest_rate, 4),
                'today_calls': today_calls,
                'today_connected': today_connected
            },
            'recent_packages': [pkg.to_dict() for pkg in recent_packages]
        }
    })


@metrics_bp.route('/summary', methods=['GET'])
def get_metrics_summary():
    """
    获取指标汇总
    
    查询参数:
        - start_date: 开始日期 (YYYY-MM-DD)
        - end_date: 结束日期 (YYYY-MM-DD)
    """
    # 获取日期范围
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    
    query = MetricsSummary.query
    
    if start_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        query = query.filter(MetricsSummary.date >= start_date)
    
    if end_date_str:
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        query = query.filter(MetricsSummary.date <= end_date)
    
    # 排序：最新的在前
    summaries = query.order_by(MetricsSummary.date.desc()).all()
    
    return jsonify({
        'success': True,
        'data': [summary.to_dict() for summary in summaries]
    })


@metrics_bp.route('/summary/today', methods=['POST'])
def calculate_today_summary():
    """计算今日指标汇总"""
    summary = MetricsSummary.calculate_today_metrics()
    
    return jsonify({
        'success': True,
        'data': summary.to_dict(),
        'message': '今日指标计算成功'
    })


@metrics_bp.route('/trends', methods=['GET'])
def get_trends():
    """
    获取趋势数据（最近7天、30天）
    
    查询参数:
        - days: 天数 (默认 7)
    """
    days = request.args.get('days', 7, type=int)
    
    # 计算日期范围
    end_date = date.today()
    start_date = end_date - timedelta(days=days-1)
    
    # 查询汇总数据
    summaries = MetricsSummary.query.filter(
        MetricsSummary.date >= start_date,
        MetricsSummary.date <= end_date
    ).order_by(MetricsSummary.date.asc()).all()
    
    # 如果数据不完整，填充缺失的日期
    date_map = {s.date: s for s in summaries}
    trends = []
    
    current_date = start_date
    while current_date <= end_date:
        if current_date in date_map:
            trends.append(date_map[current_date].to_dict())
        else:
            # 填充空数据
            trends.append({
                'date': current_date.isoformat(),
                'total_packages': 0,
                'total_calls': 0,
                'connected_calls': 0,
                'avg_contact_rate': 0.0
            })
        current_date += timedelta(days=1)
    
    return jsonify({
        'success': True,
        'data': trends
    })


@metrics_bp.route('/package/<int:package_id>/stats', methods=['GET'])
def get_package_stats(package_id):
    """
    获取单个数据包的详细统计
    
    返回:
        - 基本信息
        - 外呼任务统计
        - 通话结果分布
        - 标签统计
    """
    package = LeadPackage.query.get_or_404(package_id)
    
    # 统计外呼任务
    tasks = package.dial_tasks.all()
    total_tasks = len(tasks)
    completed_tasks = sum(1 for t in tasks if t.status == 'completed')
    
    # 统计所有通话记录
    all_calls = []
    for task in tasks:
        all_calls.extend(task.calls.all())
    
    total_calls = len(all_calls)
    
    # 通话结果分布
    result_distribution = {}
    for call in all_calls:
        result = call.result
        result_distribution[result] = result_distribution.get(result, 0) + 1
    
    # 获取标签汇总
    tag_summaries = [s.to_dict() for s in package.tag_summaries.all()]
    
    return jsonify({
        'success': True,
        'data': {
            'package': package.to_dict(),
            'task_stats': {
                'total': total_tasks,
                'completed': completed_tasks,
                'in_progress': sum(1 for t in tasks if t.status == 'in_progress'),
                'pending': sum(1 for t in tasks if t.status == 'pending')
            },
            'call_stats': {
                'total': total_calls,
                'result_distribution': result_distribution
            },
            'tag_summaries': tag_summaries
        }
    })


@metrics_bp.route('/export', methods=['GET'])
def export_metrics():
    """
    导出指标数据（CSV 格式）
    
    查询参数:
        - start_date: 开始日期
        - end_date: 结束日期
        - format: 导出格式 (csv/json)
    """
    # TODO: 实现 CSV 导出功能
    return jsonify({
        'success': False,
        'error': '导出功能开发中'
    }), 501

