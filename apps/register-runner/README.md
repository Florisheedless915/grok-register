# register-runner

注册执行器模块。

当前仓库里真正承担注册动作的仍然是根目录下的 [DrissionPage_example.py](/home/codex/grok-register/DrissionPage_example.py) 和 [email_register.py](/home/codex/grok-register/email_register.py)。控制台新建任务时，会把这两份运行文件复制到独立任务目录，再按任务配置生成 `config.json` 后执行。

这个目录保留为后续拆分点，职责建议固定为：

- 接收编排层下发的任务参数
- 准备运行目录、浏览器环境和日志目录
- 执行注册主流程
- 产出 `sso`、运行日志和状态事件

当前闭环里它对应的实际文件：

- 主流程：[DrissionPage_example.py](/home/codex/grok-register/DrissionPage_example.py)
- 邮箱适配：[email_register.py](/home/codex/grok-register/email_register.py)
- 浏览器补丁：[turnstilePatch/script.js](/home/codex/grok-register/turnstilePatch/script.js)
