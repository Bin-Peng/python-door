from typing import Optional
from task_manager import TaskManager


class TaskCLI:
    def __init__(self):
        # 初始化任务管理器
        self.task_manager = TaskManager()

    def add_task(self) -> None:
        # 添加任务的命令行界面
        print("\n=== 添加新任务 ===")
        # 获取用户输入的任务标题
        title = input("请输入任务标题: ").strip()
        # 获取用户输入的任务描述
        description = input("请输入任务描述: ").strip()

        # 检查输入是否为空
        if not title or not description:
            print("错误：任务标题和描述不能为空！")
            return

        # 添加新任务
        task = self.task_manager.add_task(title, description)
        print(f"\n成功添加任务！任务ID: {task.id}")

    def edit_task(self) -> None:
        # 编辑任务的命令行界面
        print("\n=== 编辑任务 ===")
        # 获取用户输入的任务ID
        task_id_input = input("请输入要编辑的任务ID: ").strip()

        # 验证任务ID输入
        if not task_id_input.isdigit():
            print("错误：请输入有效的任务ID（数字）！")
            return

        task_id = int(task_id_input)

        # 获取新的任务信息（允许为空，表示不修改）
        print("\n请输入新的任务信息（直接按回车表示不修改）：")
        title = input("新的任务标题: ").strip()
        description = input("新的任务描述: ").strip()
        completed_input = input("是否完成 (y/n，直接按回车表示不修改): ").strip().lower()

        # 处理完成状态输入
        completed: Optional[bool] = None
        if completed_input in ['y', 'yes']:
            completed = True
        elif completed_input in ['n', 'no']:
            completed = False

        # 更新任务
        updated_task = self.task_manager.edit_task(
            task_id,
            title if title else None,
            description if description else None,
            completed
        )

        if updated_task:
            print("\n任务更新成功！")
            print(f"标题: {updated_task.title}")
            print(f"描述: {updated_task.description}")
            print(f"状态: {'已完成' if updated_task.completed else '未完成'}")
        else:
            print(f"\n错误：未找到ID为 {task_id} 的任务！")

    def run(self) -> None:
        # 主程序循环
        while True:
            print("\n=== 任务管理器 ===")
            print("1. 添加任务")
            print("2. 编辑任务")
            print("3. 退出")

            choice = input("\n请选择操作 (1-3): ").strip()

            if choice == "1":
                self.add_task()
            elif choice == "2":
                self.edit_task()
            elif choice == "3":
                print("\n感谢使用！再见！")
                break
            else:
                print("\n无效的选择，请重试！")


def main():
    # 程序入口点
    cli = TaskCLI()
    cli.run()


if __name__ == "__main__":
    main()
