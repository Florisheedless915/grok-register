# Grok Register

面向 `x.ai` 注册批处理的一体化项目。

这个仓库现在不是单一脚本仓库，而是一个“统一项目、内部解耦”的闭环方案，包含：

- `network`：WARP / 代理桥接
- `register`：注册执行器
- `sink`：把成功结果推到 `grok2api` 等下游
- `console`：任务创建、状态监控、日志查看
- `worker-runtime`：`Xvfb + Chrome/Chromium + Python` 运行环境定义

## 你能直接用它做什么

- 命令行直接跑注册
- 在 Web 控制台里创建批量任务
- 给每个任务独立配置出口、邮箱参数和 sink
- 实时查看每个任务的轮次、成功数、失败数和日志
- 注册成功后自动把 `sso` 推入 `grok2api` 兼容接口

## 项目结构

- [apps/console](/home/codex/grok-register/apps/console)：控制台
- [apps/network-gateway](/home/codex/grok-register/apps/network-gateway)：前置网络出口约定
- [apps/register-runner](/home/codex/grok-register/apps/register-runner)：执行器模块说明
- [apps/token-sink](/home/codex/grok-register/apps/token-sink)：结果落池说明
- [apps/worker-runtime](/home/codex/grok-register/apps/worker-runtime)：运行时环境定义
- [deploy](/home/codex/grok-register/deploy)：启动脚本和部署骨架
- [docs](/home/codex/grok-register/docs)：架构、流程、快速开始、配置说明
- [DrissionPage_example.py](/home/codex/grok-register/DrissionPage_example.py)：当前主执行脚本
- [email_register.py](/home/codex/grok-register/email_register.py)：临时邮箱适配层

## 快速入口

- 新手先看 [docs/quickstart.md](/home/codex/grok-register/docs/quickstart.md)
- 想看完整链路看 [docs/business-flow.md](/home/codex/grok-register/docs/business-flow.md)
- 想弄清楚字段含义看 [docs/options.md](/home/codex/grok-register/docs/options.md)
- 想看模块边界看 [docs/architecture.md](/home/codex/grok-register/docs/architecture.md)

## 命令行运行

```bash
cd /home/codex/grok-register
cp config.example.json config.json
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python DrissionPage_example.py --count 1
```

## 控制台运行

```bash
cd /home/codex/grok-register
./deploy/start-console.sh
```

默认监听 `0.0.0.0:18600`。

## 当前配置模板

```json
{
  "run": {
    "count": 50
  },
  "temp_mail_api_base": "https://mail-api.example.com",
  "temp_mail_admin_password": "<your_admin_password>",
  "temp_mail_domain": "mail.example.com",
  "temp_mail_site_password": "",
  "proxy": "",
  "browser_proxy": "",
  "api": {
    "endpoint": "http://127.0.0.1:18000/api/v1/admin/tokens",
    "token": "",
    "append": true
  }
}
```

说明：

- 仓库里的模板已经去掉个人邮箱和个人域名
- `config.json` 仍然不入库，避免把生产凭据提交到仓库
- 代码仍兼容旧的 `duckmail_*` 字段，但新部署建议统一使用 `temp_mail_*`

## 闭环要求

只有下面 4 段都通，业务才算真正能跑批：

1. 网络出口通：`browser_proxy` / `proxy`
2. 临时邮箱通：`temp_mail_api_base` / `temp_mail_domain`
3. 注册执行通：浏览器、`Xvfb`、Python 依赖齐全
4. sink 通：`api.endpoint` / `api.token`

## 兼容性说明

- 根目录命令行脚本继续保留，可直接使用
- 新增控制台和模块目录不会接管你现有生产目录
- 控制台任务全部运行在 `apps/console/runtime/tasks/` 下的独立目录里

## 致谢

- 感谢 [XeanYu](https://github.com/XeanYu) 和 [chenyme](https://github.com/chenyme) 的开源项目与思路，这个仓库是在他们相关工作的基础上继续整理、集成和工程化。
- [kevinr229/grok-maintainer](https://github.com/kevinr229/grok-maintainer)
- [DrissionPage](https://github.com/g1879/DrissionPage)
- [grok2api](https://github.com/chenyme/grok2api)
