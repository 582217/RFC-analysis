# RFC-analysis


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

**RFC重要性量化：**  
  std-level √  
  草案迭代次数 √  
  搜索引擎返回的结果数 √


**寻找最新热点：**  

  方法1：  
  直接从工作组agenda获取近几个月的热点    
  https://tools.ietf.org/wg/dnsop/agenda  
  方法2：  
  从工作组邮件列表分析近一个月的邮件的讨论次数，讨论较多的为热点      
  https://mailarchive.ietf.org/arch/browse/dnsop/ past month, thread, [@id="message-thread"]  


**寻找曾是热点的废弃草案：**  

  1.获取所有废弃草案名  
  2.查询所有废弃草案的迭代次数和最终状态     
    https://datatracker.ietf.org/doc/draft-ietf-dnsext-rfc2536bis-dsa  json  


**关键词提取和主题建模**
