# NJU Mihomo Rules

从 EZ4Connect / ZJU Connect 日志中整理的南京大学 Mihomo IP 分流规则集。

## 规则集

| 文件 | 用途 | 建议 |
| --- | --- | --- |
| `rules/nju-campus.yaml` | 南京大学公网地址 | 默认启用 |
| `rules/nju-private.yaml` | VPN 下发的私有地址 | 按需启用，可能和家庭、公司或容器网络冲突 |
| `rules/academic-domains.yaml` | 常见中外文学术平台域名 | 按需启用，通过学校出口访问订阅资源 |
| `dist/v2rayn/nju-incremental.json` | v2rayN 增量路由 | 合并进已有路由，不含兜底 |
| `dist/v2rayn/nju-proxy-direct.json` | v2rayN 完整路由 | 学术与校园流量走当前节点，其余直连 |
| `dist/sing-box/*.json` | sing-box source rule-set | 可远程引用或编译为 SRS |

`nju-campus.yaml` 保留了原始路由对 `219.219.118.25` 的排除。该地址是日志中选中的 VPN 接入节点，把它重新送进 VPN 可能形成路由回环。

## Mihomo 配置

```yaml
rule-providers:
  nju-campus:
    type: http
    behavior: ipcidr
    format: yaml
    url: https://raw.githubusercontent.com/Miraitowa2001/nju-mihomo-rules/main/rules/nju-campus.yaml
    path: ./ruleset/nju-campus.yaml
    interval: 86400

  # 可选：可能与本地私网冲突
  nju-private:
    type: http
    behavior: ipcidr
    format: yaml
    url: https://raw.githubusercontent.com/Miraitowa2001/nju-mihomo-rules/main/rules/nju-private.yaml
    path: ./ruleset/nju-private.yaml
    interval: 86400

  academic-domains:
    type: http
    behavior: domain
    format: yaml
    url: https://raw.githubusercontent.com/Miraitowa2001/nju-mihomo-rules/main/rules/academic-domains.yaml
    path: ./ruleset/academic-domains.yaml
    interval: 86400

rules:
  # 必须放在私网直连、GEOIP,CN 和 MATCH 之前
  - RULE-SET,nju-campus,南大VPN,no-resolve
  # - RULE-SET,nju-private,南大VPN,no-resolve
  - RULE-SET,academic-domains,南大VPN
  - MATCH,默认策略
```

`南大VPN` 必须是你的配置中实际存在的策略组或出站名称。

## v2rayN

v2rayN 的 `proxy` 指当前选中的服务器。先把 EZ4Connect 的
`127.0.0.1:11080` 添加为 SOCKS 服务器并设为当前服务器，然后打开：

1. 设置 → 路由设置 → 添加规则集；
2. 在规则集编辑页填写下面的 URL；
3. 选择“从订阅 URL 中导入规则”；
4. 将该规则集设为活动路由。

完整模式 URL：

```text
https://raw.githubusercontent.com/Miraitowa2001/nju-mihomo-rules/main/dist/v2rayn/nju-proxy-direct.json
```

若要合并到已有规则，使用增量 URL：

```text
https://raw.githubusercontent.com/Miraitowa2001/nju-mihomo-rules/main/dist/v2rayn/nju-incremental.json
```

增量规则必须放在通用私网直连、国内直连和最终兜底之前。受 v2rayN
出站模型限制，它不能在普通路由界面中同时选择“NJU 节点”和另一机场节点。

## sing-box

`dist/sing-box/` 提供官方 source rule-set JSON。可直接作为远程规则集使用，
也可执行 `sing-box rule-set compile` 编译为二进制 `.srs`。

## 从新日志更新

仓库以 `data/*.txt` 为源数据，运行：

```shell
python scripts/build.py
python scripts/build.py --check
```

也可从新日志列出所有下发路由，人工确认归属后再更新源数据：

```shell
python scripts/extract_routes.py path/to/ez4connect.log
```

脚本只负责忠实提取，不会自动把第三方数据库、出版社或 CDN 地址判定为南大网段。

## 数据边界

当前规则来自一次实际连接的服务端下发路由，不是南京大学官方公布的完整地址清单。日志中的大量 `/32` 地址属于校外学术资源或第三方服务，未并入校园网规则。

## License

MIT
