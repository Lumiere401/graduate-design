import matplotlib.pyplot as plt
import numpy as np
import csv


# #函数
# g=lambda z:np.maximum(0.01*z,z)
#
# start=-100 #输入需要绘制的起始值（从左到右）
# stop=50 #输入需要绘制的终点值
# step=0.01#输入步长
# num=(stop-start)/step #计算点的个数
# x = np.linspace(start,stop,int(num))
# y = g(x)
#
# fig=plt.figure(1)
# plt.plot(x, y,label='relu')
# plt.grid(True)#显示网格
#
# plt.legend()#显示旁注
# plt.show()


exampleFile = open('tag-accuracy.csv')  # 打开csv文件
exampleReader = csv.reader(exampleFile)  # 读取csv文件
exampleData = list(exampleReader)  # csv数据转换为列表
length_zu = len(exampleData)  # 得到数据行数
length_yuan = len(exampleData[0])  # 得到每行长度

# for i in range(1,length_zu):
#     print(exampleData[i])

x = list()
y = list()

for i in range(1, length_zu):  # 从第二行开始读取
    x.append(exampleData[i][0])  # 将第一列数据从第二行读取到最后一行赋给列表x
    y.append(exampleData[i][1])  # 将第二列数据从第二行读取到最后一行赋给列表
fig, ax = plt.subplots(1, 2)
axes = ax.flatten()
lns1 = axes[0].plot(x, y, label="Loss")
# 按一定间隔显示实现方法
# ax2.plot(200 * np.arange(len(fig_accuracy)), fig_accuracy, 'r')
# lns2 = axes[1].plot(np.arange(train_epochs / 10), fig_accuracy, 'r', label="Accuracy")
axes[0].set_xlabel('iteration')
axes[0].set_ylabel('training loss')
axes[1].set_xlabel('iteration')
axes[1].set_ylabel('training accuracy')
plt.savefig('loss_acc.png')
plt.plot(x, y)  # 绘制x,y的折线图
plt.show()  # 显示折线图

