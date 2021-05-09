# SystemInfo
一个MCDR插件,用于查看系统信息和资源占用情况。

命令：`!!sysinfo`  
~~需要安装依赖`pip install psutil`~~  
MCDR 1.x 已自带这个库，所以无需安装。

## 修改显示项目
用你喜欢的编辑器打开 `SysInfo.py`。你可以轻而易举地在第 8 行找到显示项目列表。修改它即可达成任何你想要的效果。
```python
info_list = [
        f"{'='*10}服务器信息{'='*10}",
        get_system(), # 系统类型
        get_cpu_usage(), # CPU占用
        get_memory(), # 内存占用
        get_disk_usage(), # 磁盘占用
        get_java_usage(source.get_server()), # 服务端占用
        '='*28
    ]
```
