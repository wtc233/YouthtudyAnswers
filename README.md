# YouthtudyAnswers
青学Answers - 自动获取青年大学习最新一期或偷跑一期的答案并导出为HTML。

## DEMO
[青学Answers](http://www.daixia.hu)

## 准备工作
需要环境：Python3  
需要库：requests、lxml

## 如何使用
运行方式：`cd`至程序目录并`python`运行`YouthtudyAnswers.py`程序  
例：`cd /www && python3 ./YouthtudyAnswers.py`

可选附加参数：`last`用于获取偷跑一期  
例：`cd /www && python3 ./YouthtudyAnswers.py last`

运行后会生成`index.html`或`last.html`用于在网站上显示答案。

## 已适配功能：  
- 选择题答案自查
- 拖动题答案自查
- 课后题自动区别

## License
[GNU General Public License v3.0](https://github.com/mlgexyz/YouthtudyAnswers/blob/master/LICENSE) © [mlge](https://github.com/mlgexyz)
