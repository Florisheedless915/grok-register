# token-sink

结果落池模块。

默认对接 [grok2api](https://github.com/chenyme/grok2api) 兼容的管理接口。注册成功后，执行器会把新增 `sso` token 推送到 `api.endpoint`。

当前约定：

- `api.endpoint`：token 管理接口，例如 `http://127.0.0.1:18000/api/v1/admin/tokens`
- `api.token`：管理口令
- `api.append=true`：先读取存量再去重合并，保护已有 token
- `api.append=false`：直接以本次结果覆盖远端数据

建议后续继续在这里收敛的功能：

- token 入池结果校验
- 可选回写运行统计
- 死信重试
- 多个 sink 目标并发推送
