# RFC-analysis

## 用机器学习预测热点是否可行 

如何定义热点，如果说某个方向是热点，这个方向的范围要画多大？


**目前感觉可行的办法**：作为分类问题研究， 寻找草案的特征和其归宿（成为STD，RFC，或是流产）的关系， 最终获得一个分类器，预测当前的草案，分为有前途和没前途。

**该办法需要解决的问题**：需要草案和RFC的对应关系，需要草案清晰的特征，需要对其归宿的评价

## 待解决问题：

~~怎么取得RFC和草案的对应关系？~~

~~怎么知道一个RFC前有多少草案？~~

~~一篇草案的历程是怎样的？改名怎么处理？（使用局部敏感哈希？）~~

有哪些特征？数量，频率，篇幅，工作组（工作组实力如何量化），AD，主题，关键词，年代。。。？

如何评价RFC的重要性？类型，工作组，作者，被引次数，~~专利，被更新次数~~，谷歌搜索结果数。。。？

不止于草案，也加入邮件列表内容要怎么处理？ **邮件列表讨论频率更能反映出热点**  
https://datatracker.ietf.org/list/wg/   工作组邮件列表


## 目前完成的工作：

**rfc_infor.py**

建立RFC数据库：编号，题目，日期，Stream，领域，子领域，关键词，工作组，**Status,变为RFC前的草案数**

**dns_plot.py**

绘制DNS相关RFC的图表，包括:

年份-数量 折线图

工作组-领域-数量 热力图

领域-数量 工作组-数量 Stream-数量 Status-数量 条形图

**mail_infor.py**

获取工作组的邮件总数和时间跨度

## 这一周要做的工作


获取每个RFC的谷歌搜索结果数 （怎么解析JS？）



