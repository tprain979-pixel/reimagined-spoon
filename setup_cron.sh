#!/bin/bash
# 自动设置 cron 定时任务脚本

echo "=========================================="
echo "欧洲物流预警系统 - Cron 定时任务设置"
echo "=========================================="
echo ""

# 获取当前目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_PATH=$(which python3)

echo "📂 项目目录: $SCRIPT_DIR"
echo "🐍 Python 路径: $PYTHON_PATH"
echo ""

# 创建日志目录
mkdir -p "$SCRIPT_DIR/logs"
echo "✅ 日志目录已创建: $SCRIPT_DIR/logs"
echo ""

# 生成 crontab 配置
echo "📝 生成 crontab 配置..."
echo ""

# 方案选择
echo "请选择定时任务方案："
echo "  1) 每天 1 次（节省模式）- 08:00 天气，09:00 新闻"
echo "  2) 每天 2 次（推荐模式）- 08:00, 18:00 天气，09:00, 19:00 新闻"
echo "  3) 每天 4 次（高频模式）- 每 6 小时一次"
echo ""
read -p "请输入选项 [1-3]: " choice

case $choice in
    1)
        echo ""
        echo "已选择：节省模式（每天 1 次）"
        echo "配额消耗：60 次/月（6%）"
        echo ""
        CRON_CONFIG="# 欧洲物流预警系统 - 每天 1 次
0 8 * * * cd $SCRIPT_DIR && $PYTHON_PATH logistics_alert_full.py weather >> $SCRIPT_DIR/logs/weather.log 2>&1
0 9 * * * cd $SCRIPT_DIR && $PYTHON_PATH logistics_alert_full.py news >> $SCRIPT_DIR/logs/news.log 2>&1"
        ;;
    2)
        echo ""
        echo "已选择：推荐模式（每天 2 次）"
        echo "配额消耗：120 次/月（12%）"
        echo ""
        CRON_CONFIG="# 欧洲物流预警系统 - 每天 2 次
0 8 * * * cd $SCRIPT_DIR && $PYTHON_PATH logistics_alert_full.py weather >> $SCRIPT_DIR/logs/weather.log 2>&1
0 9 * * * cd $SCRIPT_DIR && $PYTHON_PATH logistics_alert_full.py news >> $SCRIPT_DIR/logs/news.log 2>&1
0 18 * * * cd $SCRIPT_DIR && $PYTHON_PATH logistics_alert_full.py weather >> $SCRIPT_DIR/logs/weather.log 2>&1
0 19 * * * cd $SCRIPT_DIR && $PYTHON_PATH logistics_alert_full.py news >> $SCRIPT_DIR/logs/news.log 2>&1"
        ;;
    3)
        echo ""
        echo "已选择：高频模式（每天 4 次）"
        echo "配额消耗：240 次/月（24%）"
        echo ""
        CRON_CONFIG="# 欧洲物流预警系统 - 每天 4 次
0 6 * * * cd $SCRIPT_DIR && $PYTHON_PATH logistics_alert_full.py weather >> $SCRIPT_DIR/logs/weather.log 2>&1
30 6 * * * cd $SCRIPT_DIR && $PYTHON_PATH logistics_alert_full.py news >> $SCRIPT_DIR/logs/news.log 2>&1
0 12 * * * cd $SCRIPT_DIR && $PYTHON_PATH logistics_alert_full.py weather >> $SCRIPT_DIR/logs/weather.log 2>&1
30 12 * * * cd $SCRIPT_DIR && $PYTHON_PATH logistics_alert_full.py news >> $SCRIPT_DIR/logs/news.log 2>&1
0 18 * * * cd $SCRIPT_DIR && $PYTHON_PATH logistics_alert_full.py weather >> $SCRIPT_DIR/logs/weather.log 2>&1
30 18 * * * cd $SCRIPT_DIR && $PYTHON_PATH logistics_alert_full.py news >> $SCRIPT_DIR/logs/news.log 2>&1
0 22 * * * cd $SCRIPT_DIR && $PYTHON_PATH logistics_alert_full.py weather >> $SCRIPT_DIR/logs/weather.log 2>&1
30 22 * * * cd $SCRIPT_DIR && $PYTHON_PATH logistics_alert_full.py news >> $SCRIPT_DIR/logs/news.log 2>&1"
        ;;
    *)
        echo "❌ 无效的选项，退出"
        exit 1
        ;;
esac

# 保存到临时文件
echo "$CRON_CONFIG" > /tmp/logistics_cron.txt
echo "✅ Cron 配置已生成"
echo ""

# 显示配置内容
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "生成的 Cron 配置："
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
cat /tmp/logistics_cron.txt
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 询问是否安装
read -p "是否将以上配置添加到 crontab？[y/N]: " confirm

if [[ $confirm =~ ^[Yy]$ ]]; then
    # 备份现有 crontab
    crontab -l > /tmp/crontab_backup_$(date +%Y%m%d_%H%M%S).txt 2>/dev/null || true
    echo "✅ 已备份现有 crontab"

    # 添加新配置
    (crontab -l 2>/dev/null; echo ""; cat /tmp/logistics_cron.txt) | crontab -
    echo "✅ Cron 定时任务已设置"
    echo ""

    # 验证
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "当前 crontab 配置："
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    crontab -l | tail -10
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "🎉 设置完成！"
    echo ""
    echo "📋 下一步："
    echo "  - 系统将在设定时间自动执行"
    echo "  - 查看日志: tail -f $SCRIPT_DIR/logs/*.log"
    echo "  - 手动测试: python $SCRIPT_DIR/logistics_alert_full.py both"
else
    echo ""
    echo "❌ 已取消设置"
    echo ""
    echo "📝 手动设置方法："
    echo "  1. 运行: crontab -e"
    echo "  2. 复制以下内容："
    echo ""
    cat /tmp/logistics_cron.txt
    echo ""
    echo "  3. 保存退出 (ESC → :wq)"
fi

echo ""
echo "=========================================="
