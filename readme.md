# Grok Register

面向 `x.ai` 注册批处理的一体化项目，提供控制台、注册执行器、运行时环境和 token 落池能力。

## 功能

- 命令行直接跑注册
- 在 Web 控制台里创建批量任务
- 给每个任务独立配置出口、邮箱参数和 sink
- 实时查看每个任务的轮次、成功数、失败数和日志
- 注册成功后自动把 `sso` 推入 `grok2api` 兼容接口

## 先决条件

这个项目要跑通，至少要有下面 3 个外部条件：

- 可用的网络出口，例如 WARP / 代理桥接
- 可被 `x.ai` 接受的临时邮箱域名
- 可接收 token 的下游 sink，例如 `grok2api`

如果这 3 段没有准备好，项目本身能启动，但注册链路不会真正闭环。

## 最快启动方式

推荐第一次使用直接走 Docker。

```bash
git clone https://github.com/509992828/grok-register.git
cd grok-register
docker compose up -d --build
```

启动后访问：

- `http://<你的服务器IP>:18600`

然后在控制台里填写：

- `browser_proxy`
- `proxy`
- `temp_mail_api_base`
- `temp_mail_admin_password`
- `temp_mail_domain`
- `api.endpoint`
- `api.token`

## 宿主机启动方式

```bash
cp config.example.json config.json
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
./deploy/start-console.sh
```

默认监听 `0.0.0.0:18600`。

## 命令行验证

在真正跑批之前，建议先用一次单轮验证检查链路：

```bash
cp config.example.json config.json
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python DrissionPage_example.py --count 1
```

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

配置模板说明：

- 仓库里提供的是可公开分享的示例配置，不包含任何真实邮箱接口、真实域名、密码或 token
- 实际运行时，请把你自己的参数写进本机 `config.json` 或控制台系统配置里，不要把生产凭据提交回仓库
- 代码兼容旧版 `duckmail_*` 字段，只是为了照顾历史配置；第一次部署的新用户，直接使用 `temp_mail_*` 这一套字段即可

## 文档入口

- 新手快速上手：[docs/quickstart.md](docs/quickstart.md)
- 完整业务链路：[docs/business-flow.md](docs/business-flow.md)
- 配置字段说明：[docs/options.md](docs/options.md)
- 模块边界和架构：[docs/architecture.md](docs/architecture.md)

## 项目结构

- [apps/console](apps/console)：控制台
- [apps/network-gateway](apps/network-gateway)：前置网络出口约定
- [apps/register-runner](apps/register-runner)：执行器模块说明
- [apps/token-sink](apps/token-sink)：结果落池说明
- [apps/worker-runtime](apps/worker-runtime)：运行时环境定义
- [deploy](deploy)：启动脚本和部署骨架
- [docs](docs)：架构、流程、快速开始、配置说明
- [DrissionPage_example.py](DrissionPage_example.py)：当前主执行脚本
- [email_register.py](email_register.py)：临时邮箱适配层

## 兼容性说明

- 根目录命令行脚本继续保留，可直接使用
- 新增控制台和模块目录不会接管你现有生产目录
- 控制台任务全部运行在 `apps/console/runtime/tasks/` 下的独立目录里

## 致谢

- 感谢 [ReinerBRO](https://github.com/ReinerBRO) 对仓库整理、部署验证和整合方向的推动。
- 感谢 [XeanYu](https://github.com/XeanYu) 和 [chenyme](https://github.com/chenyme) 的开源项目与思路，这个仓库是在他们相关工作的基础上继续整理、集成和工程化。
- [kevinr229/grok-maintainer](https://github.com/kevinr229/grok-maintainer)
- [DrissionPage](https://github.com/g1879/DrissionPage)
- [grok2api](https://github.com/chenyme/grok2api)
