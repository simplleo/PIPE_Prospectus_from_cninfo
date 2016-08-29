# PIPE_Prospectus_from_cninfo

# 1、项目目的：
# 获取非公开发行报告书、重组配套融资报告书的概要部分

# 2、代码思路简介：
# 根据给定的日期区间（get_dateRange())，从巨潮网取得区间内的所有A股公告（get_cninfo_anmt_page())，筛选其中名称符合特定条件的，筛选出重组并配套融资报告书、非公开发行报告书（check()）。
# 随后到和讯网（hexun.com）找到这篇报告书的url（get_HX_anmt_url），获取报告书的全文（get_HX_page、get_anmtHX_fulltext）并进行格式优化（巨潮上只有pdf，hexun有text）。
# 之后，根据报告书的不同类型（非公开发行、重组配套融资），在全文中提取交易概要部分（get_anmt_summary）。
# 最后，按照一定格式输出到txt文件中（class foutput）。

# 3、运行环境：win7，python3.2，beautifulsoup4.4
