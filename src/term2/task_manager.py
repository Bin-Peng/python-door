import json
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


# 使用dataclass装饰器来创建Task类，简化类的定义
@dataclass
class Task:
    title: str  # 任务标题
    description: str  # 任务描述
    created_at: str  # 创建时间
    completed: bool = False  # 任务完成状态，默认为False
    id: Optional[int] = None  # 任务ID，可选参数


class TaskManager:
    def __init__(self, file_path: str = "tasks.json"):
        # 初始化TaskManager，设置存储文件路径和任务列表
        self.file_path = file_path  # 存储任务数据的文件路径
        self.tasks: List[Task] = []  # 用于存储任务的列表
        self.load_tasks()  # 加载已存在的任务

    def load_tasks(self) -> None:
        # 从JSON文件加载任务数据
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                tasks_data = json.load(f)
                # 将JSON数据转换为Task对象列表
                self.tasks = [Task(**task) for task in tasks_data]
        except FileNotFoundError:
            # 如果文件不存在，创建一个空的任务列表
            self.tasks = []

    def save_tasks(self) -> None:
        # 将任务数据保存到JSON文件
        tasks_data = [{
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "created_at": task.created_at,
            "completed": task.completed
        } for task in self.tasks]
        
        with open(self.file_path, "w", encoding="utf-8") as f:
            # 将任务数据写入文件，设置缩进格式
            json.dump(tasks_data, f, ensure_ascii=False, indent=2)

    def add_task(self, title: str, description: str) -> Task:
        # 添加新任务
        # 生成新任务的ID（使用当前任务数量加1）
        new_id = len(self.tasks) + 1
        # 创建新的Task对象
        new_task = Task(
            id=new_id,
            title=title,
            description=description,
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            completed=False
        )
        # 将新任务添加到任务列表
        self.tasks.append(new_task)
        # 保存更新后的任务列表
        self.save_tasks()
        return new_task

    def edit_task(self, task_id: int, title: Optional[str] = None, 
                  description: Optional[str] = None,
                  completed: Optional[bool] = None) -> Optional[Task]:
        # 编辑已存在的任务
        for task in self.tasks:
            if task.id == task_id:
                # 更新任务的各个字段（如果提供了新的值）
                if title is not None:
                    task.title = title
                if description is not None:
                    task.description = description
                if completed is not None:
                    task.completed = completed
                # 保存更新后的任务列表
                self.save_tasks()
                return task
        return None  # 如果未找到指定ID的任务，返回None