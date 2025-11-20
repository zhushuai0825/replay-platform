"""
Function: 定义 ORM 数据模型
Project : 全链路回放平台
Author  : Zhu Shuai
File    : models.py
Date    : 2025/11/19
Describe: 这里集中定义数据库中的所有核心表结构
"""

from sqlalchemy import Column  # SQLAlchemy 的通用字段定义
from sqlalchemy import DateTime, Integer, String, Boolean, Text  # 常见的字段类型
from sqlalchemy import ForeignKey, JSON  # 外键和 JSON 类型
from sqlalchemy.orm import relationship  # 定义模型之间的关系
from sqlalchemy.sql import func  # 使用数据库函数，比如 now()

from .databases import Base  # 导入 SQLAlchemy Base，所有模型都要继承


class TimestampMixin:
    """通用的时间戳字段，供多个表重用"""

    created_at = Column(  # 记录创建时间
        DateTime(timezone=True),
        server_default=func.now(),
        comment="记录创建时间",
    )
    updated_at = Column(  # 记录最后一次更新时间
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        comment="记录最近更新时间",
    )


class User(Base, TimestampMixin):
    """用户信息，用于权限、审计"""

    __tablename__ = "users"  # 表名
    id = Column(Integer, primary_key=True, index=True, comment="用户自增 ID")  # 主键
    username = Column(  # 用户名，唯一
        String(50),
        unique=True,
        nullable=False,
        index=True,
        comment="用户名（唯一）",
    )
    email = Column(  # 邮箱，唯一
        String(100),
        unique=True,
        nullable=False,
        index=True,
        comment="邮箱（唯一）",
    )
    hashed_password = Column(  # 加密后的密码
        String(255),
        nullable=False,
        comment="BCrypt 加密后的密码",
    )
    role = Column(  # 角色信息，user/admin
        String(50),
        default="user",
        nullable=False,
        comment="角色（user/admin）",
    )
    is_active = Column(Boolean, default=True, comment="账号是否可用")  # 状态

    traffic_files = relationship(  # 与流量文件的一对多关系
        "TrafficFile",
        back_populates="creator",
        cascade="all, delete-orphan",
    )
    replay_tasks = relationship(  # 与任务的一对多关系
        "ReplayTask",
        back_populates="creator",
        cascade="all, delete-orphan",
    )


class Environment(Base, TimestampMixin):
    """目标环境配置"""

    __tablename__ = "environments"  # 表名
    id = Column(Integer, primary_key=True, index=True, comment="环境 ID")  # 主键
    name = Column(  # 环境名称
        String(100),
        unique=True,
        nullable=False,
        index=True,
        comment="环境名称（唯一）",
    )
    base_url = Column(String(500), nullable=False, comment="请求基础 URL")  # 域名
    description = Column(String(255), nullable=True, comment="环境描述")  # 描述
    headers = Column(JSON, default=dict, comment="默认请求头")  # 默认请求头
    auth_config = Column(JSON, default=dict, comment="鉴权配置")  # 鉴权配置

    replay_tasks = relationship(  # 与任务的一对多关系
        "ReplayTask",
        back_populates="environment",
    )


class TrafficFile(Base, TimestampMixin):
    """流量文件（HAR/JSON）"""

    __tablename__ = "traffic_files"  # 表名
    id = Column(Integer, primary_key=True, index=True, comment="文件 ID")  # 主键
    filename = Column(String(255), index=True, comment="实际存储的文件名")  # 存储名
    original_filename = Column(String(255), comment="上传时的原始文件名")  # 原名
    file_path = Column(String(500), comment="文件在磁盘上的路径")  # 路径
    file_size = Column(Integer, comment="文件大小（字节）")  # 大小
    file_type = Column(String(50), comment="文件类型（json/har）")  # 类型
    description = Column(Text, nullable=True, comment="文件备注")  # 备注
    created_by = Column(  # 上传者外键
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        comment="上传者用户 ID",
    )

    creator = relationship("User", back_populates="traffic_files")  # 反向引用
    replay_tasks = relationship(  # 与任务的一对多
        "ReplayTask",
        back_populates="traffic_file",
    )


class ReplayTask(Base, TimestampMixin):
    """回放任务"""

    __tablename__ = "replay_tasks"  # 表名
    id = Column(Integer, primary_key=True, index=True, comment="任务 ID")  # 主键
    name = Column(String(200), nullable=False, index=True, comment="任务名称")  # 名称
    traffic_file_id = Column(  # 关联的流量文件 ID
        Integer,
        ForeignKey("traffic_files.id", ondelete="CASCADE"),
        nullable=False,
        comment="使用的流量文件 ID",
    )
    environment_id = Column(  # 运行环境 ID
        Integer,
        ForeignKey("environments.id", ondelete="RESTRICT"),
        nullable=False,
        comment="运行环境 ID",
    )
    created_by = Column(  # 创建者
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        comment="任务创建者用户 ID",
    )
    status = Column(  # 当前状态
        String(50),
        default="pending",
        index=True,
        comment="任务状态（pending/running/completed/failed）",
    )
    progress = Column(Integer, default=0, comment="进度百分比")  # 进度
    total_requests = Column(Integer, default=0, comment="总请求数")  # 总数
    completed_requests = Column(Integer, default=0, comment="已完成请求数")  # 完成数
    failed_requests = Column(Integer, default=0, comment="失败请求数")  # 失败数
    started_at = Column(DateTime(timezone=True), comment="开始时间")  # 开始时间
    completed_at = Column(DateTime(timezone=True), comment="结束时间")  # 结束时间
    summary = Column(Text, nullable=True, comment="任务总结或备注")  # 备注

    traffic_file = relationship("TrafficFile", back_populates="replay_tasks")  # 文件
    environment = relationship("Environment", back_populates="replay_tasks")  # 环境
    creator = relationship("User", back_populates="replay_tasks")  # 创建者
    results = relationship(  # 结果列表
        "ReplayResult",
        back_populates="task",
        cascade="all, delete-orphan",
    )


class ReplayResult(Base, TimestampMixin):
    """单条请求的比对结果"""

    __tablename__ = "replay_results"  # 表名
    id = Column(Integer, primary_key=True, index=True, comment="结果 ID")  # 主键
    task_id = Column(  # 所属任务
        Integer,
        ForeignKey("replay_tasks.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="所属任务 ID",
    )
    request_index = Column(Integer, comment="请求在文件中的顺序")  # 序号
    original_request = Column(JSON, comment="原始请求内容")  # 原请求
    original_response = Column(JSON, comment="原始响应内容")  # 原响应
    replayed_request = Column(JSON, comment="回放请求内容")  # 回放请求
    replayed_response = Column(JSON, comment="回放响应内容")  # 回放响应
    status = Column(String(50), comment="该请求的结果状态")  # 状态
    diff_details = Column(JSON, comment="差异详情 JSON")  # diff
    response_time = Column(Integer, comment="回放耗时（毫秒）")  # 耗时

    task = relationship("ReplayTask", back_populates="results")  # 反向引用任务