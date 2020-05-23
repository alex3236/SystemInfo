import psutil
import platform

def get_proc_by_id(pid):
    return psutil.Process(pid)

def get_proc_by_name(pname):
    """ get process by name
    
    return the first process if there are more than one
    """
    for proc in psutil.process_iter():
        try:
            if proc.name() == pname:
                return proc  # return if found one
        except psutil.AccessDenied:
            pass
        except psutil.NoSuchProcess:
            pass
    return None

def ps(text):
    return round((text/1024/1024),2)

def send_message(server, player, tell):
    system_info = platform.architecture()
    cpu_count = psutil.cpu_count()
    using_cpu = psutil.cpu_percent(1)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    proc = get_proc_by_name("java.exe")
    java_cpu = psutil.Process(proc.pid).cpu_percent(1)
    java_mem = proc.memory_info().rss / psutil.virtual_memory().total * 100
    java_mem = round(java_mem,2)
    output = """=============== 计算机信息 ===============
注意，以下内容可能不准确，仅供参考。

计算机系统：§b{}
CPU个数:§b{}§r  总CPU占用:§b{}%
总内存占用：§b{}%§r (§b{}MB§r/§b{}MB§r)
磁盘占用:§b{}%§r (§b{}MB§r/§b{}MB§r)

其中，JAVA 占用CPU:§b{}%§r，占用内存:§b{}%
=======================================""".format(system_info, cpu_count, using_cpu, mem.percent, ps(mem.used), ps(mem.total), 100-disk.percent, ps(disk.free), ps(disk.total), java_cpu, java_mem)
    for line in output.splitlines():
        if tell:
            server.tell(player, '[SYS] ' + line)
        else:
            print('[SYS] ' + line)

def on_info(server, info):
    if info.is_player and info.content == '!!sysinfo':
        server.tell(info.player, '[SYS]§a请稍后，正在获取中...')
        send_message(server, info.player, True)
    elif info.content == '!!sysinfo':
        print('[SYS]请稍后，正在获取中...')
        send_message(server, info.player, False)
