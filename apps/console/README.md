# console

仓库内置 Web 控制台。

它的目标是把注册任务做成“可创建、可观察、可停止、可删除”的批处理系统，同时保持和现有生产运行目录隔离。每个任务都会复制一套运行文件到独立工作目录，再按任务配置启动，不直接复用正在运行的生产目录。

## 功能

- 系统默认配置
- 新建任务
- 高级参数按任务覆盖
- 实时状态
- 实时控制台日志
- 停止任务
- 删除任务

## 默认目录

- 控制台代码：[apps/console](/home/codex/grok-register/apps/console)
- 运行数据：`apps/console/runtime/`
- 任务目录：`apps/console/runtime/tasks/task_<id>/`

## 启动

推荐直接用仓库里的启动脚本：

```bash
cd /home/codex/grok-register
./deploy/start-console.sh
```

默认环境变量：

- `GROK_REGISTER_SOURCE_DIR=/home/codex/grok-register`
- `GROK_REGISTER_PYTHON=/home/codex/grok-register/.venv/bin/python`
- `GROK_REGISTER_CONSOLE_HOST=0.0.0.0`
- `GROK_REGISTER_CONSOLE_PORT=18600`
- `GROK_REGISTER_CONSOLE_MAX_CONCURRENT_TASKS=1`

## 手工启动

```bash
cd /home/codex/grok-register/apps/console
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
GROK_REGISTER_SOURCE_DIR=/home/codex/grok-register \
GROK_REGISTER_PYTHON=/home/codex/grok-register/.venv/bin/python \
python app.py
```

## systemd 示例

参考 [grok-register-console.service.example](/home/codex/grok-register/apps/console/grok-register-console.service.example)。
