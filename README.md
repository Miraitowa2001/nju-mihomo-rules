# NJU Mihomo Rules

从 EZ4Connect / ZJU Connect 日志中整理的南京大学 Mihomo IP 分流规则集。

## 规则集

| 文件 | 用途 | 建议 |
| --- | --- | --- |
| `rules/nju-campus.yaml` | 南京大学公网地址 | 默认启用 |
| `rules/nju-private.yaml` | VPN 下发的私有地址 | 按需启用，可能和家庭、公司或容器网络冲突 |

`nju-campus.yaml` 保留了原始路由对 `219.219.118.25` 的排除。该地址是日志中选中的 VPN 接入节点，把它重新送进 VPN 可能形成路由回环。

## Mihomo 配置

将下面的 `<OWNER>` 和 `<BRANCH>` 替换为仓库所有者及分支名：

```yaml
rule-providers:
  nju-campus:
    type: http
    behavior: ipcidr
    format: yaml
    url: https://raw.githubusercontent.com/<OWNER>/nju-mihomo-rules/<BRANCH>/rules/nju-campus.yaml
    path: ./ruleset/nju-campus.yaml
    interval: 86400

  # 可选：可能与本地私网冲突
  nju-private:
    type: http
    behavior: ipcidr
    format: yaml
    url: https://raw.githubusercontent.com/<OWNER>/nju-mihomo-rules/<BRANCH>/rules/nju-private.yaml
    path: ./ruleset/nju-private.yaml
    interval: 86400

rules:
  # 必须放在私网直连、GEOIP,CN 和 MATCH 之前
  - RULE-SET,nju-campus,南大VPN,no-resolve
  # - RULE-SET,nju-private,南大VPN,no-resolve
  - MATCH,默认策略
```

`南大VPN` 必须是你的配置中实际存在的策略组或出站名称。

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
