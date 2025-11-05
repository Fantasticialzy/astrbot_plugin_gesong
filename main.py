import logging
import random
import requests
import pyodbc  # 导入SQL Server连接库
from astrbot.api.star import Context, Star, register
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.event.filter import event_message_type, EventMessageType
from astrbot.api.message_components import *

logger = logging.getLogger(__name__)

# SQL Server数据库配置 - 请根据实际情况修改
SQL_SERVER_CONFIG = {
    'server': 'localhost',  # 服务器地址
    'database': 'CF_SA_GAME',  # 数据库名
    'username': 'cf',  # 用户名
    'password': 'Luzeyang.970408',  # 密码
    'driver': '{ODBC Driver 17 for SQL Server}'  # ODBC驱动
}


def get_online_count():
    """查询CF_MIN_CU表第一条数据的CONNECT字段"""
    try:
        # 构建连接字符串
        conn_str = (
            f"DRIVER={SQL_SERVER_CONFIG['driver']};"
            f"SERVER={SQL_SERVER_CONFIG['server']};"
            f"DATABASE={SQL_SERVER_CONFIG['database']};"
            f"UID={SQL_SERVER_CONFIG['username']};"
            f"PWD={SQL_SERVER_CONFIG['password']}"
        )
        
        # 建立数据库连接
        with pyodbc.connect(conn_str) as conn:
            with conn.cursor() as cursor:
                # 执行查询 - 获取第一条数据的CONNECT字段
                cursor.execute("SELECT TOP 1 CONNECT FROM CF_MIN_CU")
                result = cursor.fetchone()
                
                if result:
                    return f"当前在线人数: {result[0]}"
                else:
                    return "未查询到在线人数数据"
                    
    except Exception as e:
        logger.error(f"数据库查询错误: {str(e)}")
        return f"查询失败: {str(e)}"


@register(
    name="GeSongBot",
    author="GeSong",
    desc="GeSongBot",
    version="1.0"  # 版本更新
)
class GameMemePlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @event_message_type(EventMessageType.ALL)
    async def on_message(self, event: AstrMessageEvent):
        msg_obj = event.message_obj
        text = msg_obj.message_str or ""

        logger.debug(f"收到消息：{text}")

        # 定义统一的消息构造函数
        def send_game_meme(text_content,):
            return event.make_result().message(text_content)
        # 1. 处理"菜单"关键词
        if "菜单" in text:
            menu_content = "1：在线人数\n2：个人信息\n3：其他"  # 使用换行符让菜单更清晰
            yield send_game_meme(menu_content)
        
        # 2. 处理在线人数相关关键词（"在线"、"zx"、"在线人数"）
        elif any(keyword in text for keyword in ["在线", "zx", "在线人数"]):
            online_info = get_online_count()
            yield send_game_meme(online_info)
        
        else:
            # 非关键词消息不处理
            return
