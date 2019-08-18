# 感应信号控制
使用SUMO进行单个路口感应信号控制仿真

### 参考资料
* <<交通管理与控制>>，徐建闽，ISBN：978-7-114-06838-6

### 基本流程和原理

![p](https://raw.githubusercontent.com/ImLaoBJie/ActuatedSignalControl/master/images/p.jpg "p")

探测器设在次要道路上（次要道路优先）：

![fc1](https://raw.githubusercontent.com/ImLaoBJie/ActuatedSignalControl/master/images/fc1.jpg "fc1")

探测器设在主要道路上（主要道路优先）：

![fc2](https://raw.githubusercontent.com/ImLaoBJie/ActuatedSignalControl/master/images/fc2.jpg "fc2")

### TODO
- [x] 主次路半感应控制
- [ ] 全感应控制 

# 演示效果

演示中的卡顿是刻意所为，为了方便观察流程图，如果不希望卡顿，可以将`main.py`中的`PAUSE`变量调小甚至设置为0。

![demo](https://raw.githubusercontent.com/ImLaoBJie/ActuatedSignalControl/master/images/demo.gif "demo")

# 快速开始

1.下载微观交通仿真软件SUMO（Simulation of Urban Mobility）：[SUMO](http://sumo.sourceforge.net/)；

2.安装`requirements.txt`中所需要的包；

3.打开`main.py`并按照需求修改下列参数：
```
ori_file_path = 'data/'  # 原始xml文件，储存在data文件夹中

running_time = 3600  # 仿真时间

SIM_INTERVAL = 0.20  # 仿真步长

PAUSE = 0.25  # 流程图停滞时间

demand = {'NTOS': 0.2, 'ETON': 0.1, 'ETOS': 0.02, 'STOE': 0.1, 'STON': 0.2}  # 各方向交通需求，每秒生成车辆概率

isMajor = True  # 探测区部署在次要道路时，设置为False，否则True

# 设置探测器距离停车线距离
if isMajor:
    detector_loc = 30.0
else:
    detector_loc = 3.0  # minimum: 3m

TIME_UNIT = 2.0  # 单位绿灯延长时间

# 主次路的最短绿灯时间
MIN_GREEN_TIME_MINOR = TIME_UNIT
MIN_GREEN_TIME_MAJOR = 30.0 + TIME_UNIT

# 主次路的绿灯极限延长时间
MAX_GREEN_TIME_MINOR = 10.0
MAX_GREEN_TIME_MAJOR = 50.0
```

* 随检测器位置而定的初期绿灯时间

检测器与停车线间距（m） | 检测器与停车线间距（m）
------------ | -------------
0～12 | 8
13～18 | 10
19～24 | 12
25～30 | 14
31～36 | 16

4.运行`main.py`。
