import platform
import psutil
import pynvml
import sys
import datetime
import requests
import winreg
from bs4 import BeautifulSoup
import time




users_count = len(psutil.users())
users_list = ",".join([u.name for u in psutil.users()])
print(u"当前有%s个用户，分别是 %s" % (users_count, users_list))
print(u"当前操作系统：",sys.platform,"名称：",platform.platform())
cpu_core=psutil.cpu_count(logical=False)
cpu_l=psutil.cpu_count(logical=1)
cpu_h=psutil.cpu_freq()
cpu_nw=psutil.cpu_percent()
cpu_u = (str(psutil.cpu_percent(1))) + '%'

key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\CentralProcessor\0")
cpu_name=winreg.QueryValueEx(key,"ProcessorNameString")
data=dict(cpu_name=cpu_name[0])
cpu_name1=str(cpu_name[2:-15]);cpu_num=str(cpu_name[-2])


print(U"CPU：%s"%cpu_num,"\nCPU核心数：",cpu_core,"\nCPU线程数：",cpu_l,"\nCPU主频:",str(round((cpu_h.current)/1000,1))+'GHz')
print("当前CPU使用率",cpu_u)
print("CPU当前最大主频：",str(round(int(cpu_h.max)/1000,1))+'GHZ',"最小频率:",str(cpu_h.min)+'GHz')

#ram
f_ram = str(round(psutil.virtual_memory().free / (1024.0 * 1024.0 * 1024.0), 2))
a_ram=str(round(psutil.virtual_memory().total/(1024*1024*1024),2))
u_ram=int(psutil.virtual_memory().total-psutil.virtual_memory().free)/float(psutil.virtual_memory().total)
print(U"内存总量：%s GB" % a_ram,U"\n剩余内存：%s  GB" % f_ram)
ran_u1=int(u_ram*100);ran_u1=str(ran_u1)+'%'
print("内存使用率:",ran_u1)

#power
print(U"开机时间 %s" % datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"))
power_now=datetime.datetime.now()
boot_t=datetime.datetime.fromtimestamp(psutil.boot_time())
print(power_now,boot_t)
pw_s=power_now-datetime.timedelta(seconds=boot_t.second);pw_m=power_now-datetime.timedelta(minutes=boot_t.minute)
pw_h=power_now-datetime.timedelta(hours=boot_t.hour);pw_d=power_now-datetime.timedelta(days=boot_t.day)
print(U"已开机时间：%s Day %s Hours %s Min %s S"%(str(pw_d),str(pw_h),str(pw_m),str(pw_s)))

#disk
io = psutil.disk_partitions()
print("系统磁盘信息：" + str(io))
for i in io:
    disk1 = psutil.disk_usage(i.device)

print("总容量：" + str(int(disk1.total / (1024.0 * 1024.0 * 1024.0))) + "G")
print("已用容量：" + str(int(disk1.used / (1024.0 * 1024.0 * 1024.0))) + "G")
print("可用容量：" + str(int(disk1.free / (1024.0 * 1024.0 * 1024.0))) + "G")

#network
net = psutil.net_io_counters()
bytes_sent = '{0:.2f} Mb'.format(net.bytes_recv / 1024 / 1024)
bytes_rcvd = '{0:.2f} Mb'.format(net.bytes_sent / 1024 / 1024)
in_fo=psutil.net_if_addrs()
lan_fo=psutil.net_connections()
print(u"网卡接收流量 %s 网卡发送流量 %s" % (bytes_rcvd, bytes_sent))

#gpu
server_info_list = []
mat1 = 1024 * 1024
pynvml.nvmlInit()  # 初始化
gpu_device_count = pynvml.nvmlDeviceGetCount()
for gpu_index in range(gpu_device_count):
    handle = pynvml.nvmlDeviceGetHandleByIndex(gpu_index)       #handle头
    ram_gpu = pynvml.nvmlDeviceGetMemoryInfo(handle)
    server_info_list.append(
        {
            "gpu_id": gpu_index,
            "total": int(ram_gpu.total / mat1),
            "used": int(ram_gpu.used / mat1),
            "utilization": pynvml.nvmlDeviceGetUtilizationRates(handle).gpu
        }
    )
    gpu_name = str(pynvml.nvmlDeviceGetName(handle))
    gpu_temperature = pynvml.nvmlDeviceGetTemperature(handle, 0)
    gpu_f_p = pynvml.nvmlDeviceGetFanSpeed(handle)
    gpu_p = pynvml.nvmlDeviceGetPowerState(handle)
    gpu_util_rate = pynvml.nvmlDeviceGetUtilizationRates(handle).gpu
    gpu_memory_rate = pynvml.nvmlDeviceGetUtilizationRates(handle).memory
    gpu_fr=str(round(ram_gpu.total/ram_gpu.free,3))+'%';gpu_used=str(round(ram_gpu.total/ram_gpu.used,3))+'%' #g_ram data
    gpu_total=str(round(ram_gpu.total/mat1,2));gpu_free=str(round(ram_gpu.free/mat1,2));gpu_use=str(round(ram_gpu.used/mat1,2))
    print("显卡数量:",(gpu_index+1),U"显卡：%s"%gpu_name)
    print("显卡状态：\n显存总容量：%s MB"%gpu_total,U"\t已用：%s MB"%gpu_use,U"\t剩余 %s MB" %gpu_free,U"\n显存空闲率: %s \t使用率: %s"%(gpu_fr,gpu_used))
    print(U"物理状态:\n温度:%s摄氏度\t风扇速率:%s,\t供电水平:%s"%(gpu_temperature,gpu_f_p,gpu_p))
    print(U"\nGPU核显使用用率:%s\tGPU内存读写满速使用率:%s"%(str(gpu_util_rate),str(gpu_memory_rate)))
pynvml.nvmlShutdown()

time.sleep(4)
#ip
if __name__ =='__main__':
    url="https://ip.cn/api/index?ip=&type=0"
    goto=requests.get(url)
    handers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"}
    kno=goto.text
    bes=BeautifulSoup(kno,"lxml")
    net_state=goto.status_code
    net_state1=goto.raise_for_status()  #连通
    if net_state==200:
        #goto=bes.find("div",id="tab0_ip")
        ip=str(goto.text);print(ip)
        ip_loc=str(ip[28:-38]);ip_num=str(ip[-28:-15])
        print(U"公网地址为：%s 公网IP为：%s"%(ip_loc,ip_num))
    else:
        print("网络异常")



