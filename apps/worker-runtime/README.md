# worker-runtime

任务运行时环境定义。

它的目标不是取代宿主机部署，而是把注册执行器依赖的系统组件明确下来，避免“机器换了就跑不起来”。

当前运行闭环至少需要：

- `Xvfb`
- `Chrome/Chromium`
- Python 3.10+
- 根目录 [requirements.txt](/home/codex/grok-register/requirements.txt) 依赖
- 控制台则额外需要 [apps/console/requirements.txt](/home/codex/grok-register/apps/console/requirements.txt)

示例容器定义见 [Dockerfile](/home/codex/grok-register/apps/worker-runtime/Dockerfile)。
