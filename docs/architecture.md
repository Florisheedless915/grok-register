# 架构说明

这个仓库现在按“一个项目，对外统一；内部模块解耦”的方式组织。

## 模块

### 1. console

位置：[apps/console](/home/codex/grok-register/apps/console)

职责：

- Web 控制台
- 系统默认配置管理
- 新建任务
- 任务状态轮询
- 实时日志查看
- 停止和删除任务

### 2. register-runner

当前位置的实际执行器是根目录脚本：

- [DrissionPage_example.py](/home/codex/grok-register/DrissionPage_example.py)
- [email_register.py](/home/codex/grok-register/email_register.py)

职责：

- 访问 `x.ai`
- 创建邮箱
- 获取验证码
- 提交注册资料
- 抽取 `sso`
- 写本地结果
- 推送到 sink

### 3. network-gateway

位置：[apps/network-gateway](/home/codex/grok-register/apps/network-gateway)

职责：

- 托管 WARP / 代理桥接
- 为浏览器和邮箱 API 提供出口
- 在业务开始前确认网络出口可用

### 4. token-sink

位置：[apps/token-sink](/home/codex/grok-register/apps/token-sink)

职责：

- 接收注册成功后的 token
- 与 `grok2api` 这类消费端对接
- 做去重、落池和结果校验

### 5. worker-runtime

位置：[apps/worker-runtime](/home/codex/grok-register/apps/worker-runtime)

职责：

- 固化 `Xvfb + Chrome/Chromium + Python` 运行依赖
- 让不同机器上的执行环境更一致

## 设计原则

- WARP 不和注册脚本写死耦合
- sink 不直接侵入注册逻辑
- console 只做编排和观测，不直接篡改现有生产任务目录
- 每个任务都复制到自己的运行目录里执行，避免互相污染

## 当前闭环

当前仓库已经能完成下面的完整链路：

1. `network-gateway` 提供可用出口
2. `console` 创建任务并写入任务级 `config.json`
3. `register-runner` 独立执行注册流程
4. 成功后将 `sso` 追加写入本地文件
5. 同时把 `sso` 推送到 `api.endpoint`
6. `console` 持续从日志解析实时状态并展示
