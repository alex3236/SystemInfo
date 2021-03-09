import platform
import psutil
from mcdreforged.api.all import *

def get_java_proc(server: ServerInterface):
    children = psutil.Process(server.get_server_pid()).children()
    for i in children:
        if i.name.startswith('java'):
            return i

def convert_mb(text):
    return round((text/1024/1024),2)

def get_error_rtext(msg, e):
    return RTextList(msg, RText(': §c获取失败').set_hover_text(f'错误代码: \n{e}'))

def get_memory():
    try:
        mem = psutil.virtual_memory()
        mem_used = convert_mb(mem.used)
        mem_total = convert_mb(mem.total)
        return RTextList('内存占用: ', RText(f'§b{mem.percent}%§r').set_hover_text(f'§b{mem_used}MB§r/§b{mem_used}MB§r'))
    except Exception as e:
        return get_error_rtext('内存占用', e)

def get_cpu_usage():
    try:
        cpu_count = psutil.cpu_count()
        using_cpu = psutil.cpu_percent(1)
        return f'CPU个数: §b{cpu_count}§r CPU占用: §b{using_cpu}%'
    except Exception as e:
        return get_error_rtext('CPU信息', e)


def get_disk_usage():
    try:
        disk = psutil.disk_usage('/')
        disk_free = convert_mb(disk.free)
        disk_total = convert_mb(disk.total)
        return RTextList('磁盘占用: ', RText(f'§b{disk.percent}%§r').set_hover_text(f'§b{disk_free}MB§r/§b{disk_total}MB§r'))
    except Exception as e:
        return get_error_rtext('磁盘占用', e)

def get_java_usage(server: ServerInterface):
    try:
        proc = get_java_proc(server)
        java_cpu = proc.cpu_percent(1)
        java_mem_percent = round(proc.memory_info().rss / psutil.virtual_memory().total * 100, 2)
        return f'服务端 CPU 占用: §b{java_cpu}%§r 服务端内存占用: §b{java_mem_percent}%'
    except Exception as e:
        return get_error_rtext('服务端占用', e)

def get_system():
    system = platform.system()
    return '操作系统: ' + f'§b{system}§r' if system != '' else '§c未知'

def print_message(source:CommandSource, msg):
    msg = '[SYS] ' + msg
    # source.reply(msg)
    print(msg)

def send_message(source: CommandSource):
    print_message(source, '§a请稍后，正在获取中...')
    info_list = [
        f"{'='*10}服务器信息{'='*10}",
        get_system(), # 系统类型
        get_cpu_usage(), # CPU占用
        get_memory(), # 内存占用
        get_disk_usage(), # 磁盘占用
        get_java_usage(source.get_server()), # 服务端占用
        '='*30
    ]
    for i in info_list:
        print_message(source, i)

def on_load(server: ServerInterface, old_module):
    server.register_command(Literal('!!sys').runs(send_message))
    server.register_help_message('!!sys', '获取服务器信息')
