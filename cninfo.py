import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import gzip
import json
import re
from datetime import datetime, timedelta
import time
import pdb

'''
anmt的结构（cninfo）
{'announcementId': '1202564393', 'adjunctUrl': 'finalpage/2016-08-15/1202564393.PDF',
'announcementTime': 1471232440000, 'storageTime': 1471232440000, 'adjunctType': 'PDF',
'secName': '万润科技', 'announcementContent': None, 'pageColumn': '中小板',
'announcementTypeName': None, 'announcementType': 'SZZX', 'associateAnnouncement': None,
'columnId': '01010302,01010411,09020202,250201,251302', 'important': None,
'announcementTitle': '关于实际控制人及持股5%以上股东股份解除质押的公告', 'batchNum': None,
'orgId': '9900022054', 'secCode': '002654', 'id': None, 'adjunctSize': 94}

anmtHX的结构
<tr>
<td class="add2">
<a target="_blank" href="http://stockdata.stock.hexun.com/txt/stock_detail_txt_1202341257.shtml">
荣之联：关于召开2016年第二次临时股东大会的通知</a></td>
<td class="add2_1">
<a target="_blank" href="http://download.hexun.com/ftp/all_stockdata_2009/all/120\234\1202341257.PDF">
查看PDF公告</a></td>
<td class="add2_1">2016-05-27</td>
</tr>
'''


def get_dateRange():
    dateStart=datetime.today()-timedelta(days=2)
    dateEnd=datetime.today()-timedelta(days=1)
     # as "2016-07-01 ~ 2016-08-01"
    dateRange=dateStart.strftime('%Y-%m-%d')+" ~ "+dateEnd.strftime('%Y-%m-%d')
    #print(dateRange)
    #dateRange='2016-07-01 ~ 2016-07-15'
    return dateRange

def get_cninfo_anmt_page(pageNo,dateRange):
    #input page number, return the query result which is a dict
    pageURL="http://www.cninfo.com.cn/cninfo-new/announcement/query"
    myheader={
        "Accept":"application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-CN,zh;q=0.8",
        "Connection":"keep-alive",
        "Content-Length":"215",
        "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie":"JSESSIONID=FBE01542E58AAA37B2DFD8D1CFA1EEB5",
        "Host":"www.cninfo.com.cn",
        "Origin":"http://www.cninfo.com.cn",
        "Referer":"http://www.cninfo.com.cn/cninfo-new/announcement/show",
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
        "X-Requested-With":"XMLHttpRequest}"}
    urlData={
        "stock":"",
        "searchkey":"",
        "plate":"",
        "category":"",
        "trade":"",
        "column":"szse_sme",
        "columnTitle":"历史公告查询",
        "pageNum":pageNo,
        "pageSize":30,
        "tabName":"fulltext",
        "sortName":"",
        "sortType":"",
        "limit":"", 
        "showTitle":"",
        "seDate":dateRange} # as "2016-08-09 ~ 2016-08-10"}
    encoded_urlData=urllib.parse.urlencode(urlData)
    encoded_urlData=encoded_urlData.encode(encoding='UTF8')
    req = urllib.request.Request(pageURL, encoded_urlData, myheader)
    #print(req)
    oper = urllib.request.urlopen(req)
    data = oper.read()
    data=data.decode('utf-8')
    return json.loads(data)
    #print(data)

def check(anmt):
    #check if the annoucment element satisfies the key words
    anmtTitle=anmt["announcementTitle"]

    m1=re.search(r'(?P<n1>配套资金报告书（草案）)|(?P<n2>非公开发行(A股)?股票预案)',anmtTitle)
    m2=re.search(r'(审计|评估|核查|审核|摘要|回复|承诺|声明|'+\
                   '说明|停牌|进展|复牌|法律意见书|终止|限售股|'+\
                   '情况|自查|认购|提示|督导|意见|关于|对照表|对比表)',anmtTitle)
    
    if (m1 and m2 == None ):
        if m1.group('n1'):
            return 1
        elif m1.group('n2'):
            return 2
    else:
        return False
    
def get_HX_page(pageNo,secCode):
    #pageURL="http://stockdata.stock.hexun.com/2009_ggqw_"+str(secCode)+".shtml"
    pageURL="http://stockdata.stock.hexun.com/2008/ggqw.aspx?page="+\
             str(pageNo)+"&stockid="+str(secCode)
    #print(pageURL) ###
    myheader={
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding":"gzip, deflate, sdch",
        "Accept-Language":"zh-CN,zh;q=0.8",
        "Cache-Control":"max-age=0",
        "Connection":"keep-alive",
        #"Cookie":"__jsluid=2d83ca9f17f10fe33ae80c320153cc4a; Hm_lvt_cb1b8b99a89c43761f616e8565c9107f=1469715370; Hm_lpvt_cb1b8b99a89c43761f616e8565c9107f=1469715370; ASP.NET_SessionId=il2hpju5etfqdht2ugphud0e; vjuids=132eed366.155b9d30cc3.0.eabaafee; _ga=GA1.2.888191973.1466241772; hxck_webdev1_general=stocklist=300282_2|002642_2; hxck_sq_common=LoginStateCookie=; Hm_lvt_cb1b8b99a89c43761f616e8565c9107f=1469715370; Hm_lpvt_cb1b8b99a89c43761f616e8565c9107f=1469715370; vjlast=1467701464.1469715484.11; HexunTrack=SID=20160618172313146e7ae19d6045a4db189af37c71ee3bc04&CITY=11&TOWN=0; __utmt=1; __utma=194262068.888191973.1466241772.1469179645.1469715445.3; __utmb=194262068.4.10.1469715445; __utmc=194262068; __utmz=194262068.1469715445.3.3.utmcsr=stock.hexun.com|utmccn=(referral)|utmcmd=referral|utmcct=/",
        "Host":"stockdata.stock.hexun.com",
        #"If-Modified-Since":"Thu, 28 Jul 2016 14:25:40 GMT",
        "Upgrade-Insecure-Requests":"1",
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
        }

    req = urllib.request.Request(pageURL, headers=myheader)
    #print(req)
    oper = urllib.request.urlopen(req)
    data = oper.read()
    data=gzip.decompress(data).decode('gb2312')
    #print(data)
    #以上获取网页内容
    return data
    

def get_HX_anmt_url(anmt):
    secCode=anmt["secCode"]
    anmtTitle=anmt["announcementTitle"]
    anmttimeStamp=anmt["announcementTime"]/1000
    anmtDate=datetime.fromtimestamp(anmttimeStamp)
    pageNo=1
    
    while True:
        data=get_HX_page(pageNo,secCode)        
        soup= BeautifulSoup(data, 'html.parser')
        anmtTable=soup.find('table',attrs={"class": "web2"})
        #找到第一页包含所有公告的table
        #print(anmtTable) ###
        anmtList=anmtTable.find_all('tr')
        firstAnmtDateStr=anmtList[0].find_all(re.compile('t[dh]'))[2].get_text()
        lastAnmtDateStr=anmtList[-1].find_all(re.compile('t[dh]'))[2].get_text()        
        firstAnmtDate=datetime.strptime(firstAnmtDateStr,'%Y-%m-%d')
        lastAnmtDate=datetime.strptime(lastAnmtDateStr,'%Y-%m-%d')
        #判断该页第一个公告的时间是否大于目标公告，
        #如果大于，
            #则继续判断该页最后一个公告时间是否小于目标公告，
            #如果小于，则在该页寻找，否则翻页
                #如果没找到，翻页
        #否则结束
        if firstAnmtDate+timedelta(days=1)>=anmtDate:
            #加一日，是因为网页上只有日期，没有时间，当日24点之前的公告都只能算到当日0点00
            if lastAnmtDate<=anmtDate:
                for anmtHX in anmtList:
                    #遍历第一页每一条公告，与目标标题作比较
                    anmtTextHX=anmtHX.find_all(re.compile('t[dh]'))[0].get_text().strip()                                  
                    anmtStartPosition=anmtTextHX.find('：')
                    if anmtTextHX[anmtStartPosition+1:]==anmtTitle:
                        #如果:后面的内容与目标标题相同，就获取对应的URL
                        target_anmt_url=anmtHX.find_all(re.compile('t[dh]'))[0].a.get('href')
                        #print(target_anmt_url)
                        return target_anmt_url                    
                pageNo+=1
            else:
                pageNo+=1                    
        else:
            return
            
def get_anmtHX_fulltext(url):
    #print(pageURL)
    pageURL=url
    myheader={
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding":"gzip, deflate, sdch",
        "Accept-Language":"zh-CN,zh;q=0.8",
        "Cache-Control":"max-age=0",
        "Connection":"keep-alive",
        #"Cookie":"__jsluid=2d83ca9f17f10fe33ae80c320153cc4a; Hm_lvt_cb1b8b99a89c43761f616e8565c9107f=1469715370; Hm_lpvt_cb1b8b99a89c43761f616e8565c9107f=1469715370; ASP.NET_SessionId=il2hpju5etfqdht2ugphud0e; vjuids=132eed366.155b9d30cc3.0.eabaafee; _ga=GA1.2.888191973.1466241772; hxck_webdev1_general=stocklist=300282_2|002642_2; hxck_sq_common=LoginStateCookie=; Hm_lvt_cb1b8b99a89c43761f616e8565c9107f=1469715370; Hm_lpvt_cb1b8b99a89c43761f616e8565c9107f=1469715370; vjlast=1467701464.1469715484.11; HexunTrack=SID=20160618172313146e7ae19d6045a4db189af37c71ee3bc04&CITY=11&TOWN=0; __utmt=1; __utma=194262068.888191973.1466241772.1469179645.1469715445.3; __utmb=194262068.4.10.1469715445; __utmc=194262068; __utmz=194262068.1469715445.3.3.utmcsr=stock.hexun.com|utmccn=(referral)|utmcmd=referral|utmcct=/",
        "Host":"stockdata.stock.hexun.com",
        #"If-Modified-Since":"Thu, 28 Jul 2016 14:25:40 GMT",
        "Upgrade-Insecure-Requests":"1",
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
        }

    req = urllib.request.Request(pageURL, headers=myheader)
    #print(req)
    oper = urllib.request.urlopen(req)
    data = oper.read()
    data=gzip.decompress(data)
    data=data.decode('gbk') #.decode('GB2312')        


    #-----去掉非字母后面nbsp------
    data=re.sub('(?<![A-Za-z])&nbsp;','',data)
    data=re.sub('A(&nbsp;)+股','A股',data)
    #-----<br>标题后面的<br>改成\n,如果标题中出现断行，则下一行15个字以内可以连接----
    data=re.sub('<br>([第（]?[一二三四五六七八九十0-9]+(([节章）]、?)|、).{1,32}?)<br>'+\
                '(([^公第一二三四五六七八九十（1-9].{1,15}?<br>)?)',\
                '\n\\1\\4\n\n',data)
    #-----：后面的br改成\n--
    data=re.sub('<br>(.{1,10}?：.*?)<br>','\n\\1\n',data)
    #-----。后面的br改成\n------
    data=re.sub('([。;:！？])\r<br>','\\1\n\n',data)
    #去掉剩余的<br> 和\r    
    data=re.sub('<br>','',data)
    data=re.sub('\r','',data)
    
    soup= BeautifulSoup(data, 'html.parser')
    report_content=soup.find('div',attrs={"id": "newsDetail"}).get_text()
    '''
    pagetail_1=re.search('[\s\S]{45}释义(?![·\.])',report_content)
    if pagetail_1:
        slide1=pagetail_1.group(0)
        tail1=re.search('\d{2,3}([\s\S]*)释义',slide1)
        if tail1:
            tail=tail1.group(1)
            print(tail)
    else:
        print('---not found tail----')
    '''
    if len(report_content)<1000:
        #如果没有成功获取DIV的内容，则退出函数 
        return    
    else:
        return report_content

def get_anmt_content(pageURL):   
    fulltext=get_anmtHX_fulltext(pageURL)
    #print(fulltext[3000:8000])
    result=re.search('(?P<content>(\d目录(.{2,5}|第一\.{3,18})[·\.]{3}|目录[·\.]{3})([\s\S]*)[·\.]{3}\d{2,3})',fulltext)
    '''
    http://stockdata.stock.hexun.com/txt/stock_detail_txt_1202525573.shtml
    '''
    
    if result:
        content="---------目录-------\n"+\
                 result.group('content')
        content=re.sub('\d目录(?![·\.])','',content)
        content=re.sub('([·\.]\d{1,3})','\\1\n',content)        
        return content
    
def get_summaryTitle(anmtType):
    if anmtType==1:
        summaryTitle='---------重大资产重组配套融资报告概述--------'
    elif anmtType==2:
        summaryTitle='-------------非公开发行报告书概述-----------'
    return summaryTitle
       
def get_anmt_summary(pageURL,anmtType):   
    fulltext=get_anmtHX_fulltext(pageURL)
    summary=None
    #print(fulltext[3000:25000])
    if anmtType==1:
        reg='(?P<summary>(?P<o1>[第\(（]?)[一二三](?P<o2>([节章）\)](、|,|\.)?)|、)'+\
                       '本次交易(方案)?(的)?概(述|要|况)(?![·\.\d])([\s\S]*?))'+\
                       '(?P=o1)[二三四](?P=o2)(交易各方|本次交易|本次发行股份的价格和数量|标的资产估值及作价)'
    elif anmtType==2:
        reg='(?P<summary>(?P<o1>[第\(（]?)[一二](?P<o2>(([节章）\)][、,\.]?)|、))'+\
                       '(本次)?(非公开)?发行(A股)?(股票)?((方案)?(的)?概(述|要|况)\n|方案\n)'+\
                       '([\s\S]*?))'+ \
                       '(?P=o1)[二三](?P=o2)'+\
                       '(本次)?(董事会)?(会议)?(前)?(确定的|关于)?(本次)?(非公开发行)?(发行)?(对象(的)?(基本情况)?|募集资金(使|运)用(的)?可行性分析)'
    
    result=re.search(reg,fulltext)
    '''
    第二节集团公司基本情况及附条件生效股份认购合同摘要
    http://stockdata.stock.hexun.com/txt/stock_detail_txt_1202445570.shtml
    '''    
    if result:
        summary=result.group('summary')     
        if len(summary)>5000:
            summary=summary[0:5000]+'\n-----------更多内容已隐藏--------------'        
    return summary

class foutput(object):
    def __init__(self,filename):
        self.f=open(filename,'w', encoding='utf-8')
        print('--------欢迎关注每日A股重组定增概要--------')
        self.f.write('--------欢迎关注每日A股重组定增概要--------\n')
        self.contlist=[]
        self.bodylist=[]
        self.headlist=[]
    def add_head(self,content):
        print(content)
        self.headlist.append(content)
        self.headlist.append('\n')
    def add_body(self,content):
        print(content)
        self.bodylist.append(content)
        self.bodylist.append('\n\n')
    def add_cont(self,cont):
        self.contlist.append(cont)
        self.contlist.append('\n')
    def output(self):
        self.f.writelines(self.headlist)
        self.f.write('--------本文包括以下公告概要,共'+str(int(len(self.contlist)/4))+'篇-------\n\n')
        self.f.writelines(self.contlist)
        self.f.write('\n--------以下为公告概要详细情况------\n')
        self.f.writelines(self.bodylist)
    def close(self):        
        self.f.close()
        
                         
        
#######     执行    ######## 
if __name__ =="__main__":
    test=0
    if test==0:
        dateRange=get_dateRange()
        anmtNum=get_cninfo_anmt_page(1,dateRange)["totalAnnouncement"]
        
        filename=r'd:\Anmt'+dateRange+r'.txt'
        f=foutput(filename)
        f.add_head('在'+ dateRange+ '期间共有'+str(anmtNum) +'篇公告，其中定增及重组报告如下：\n')
        
        for pageNum in range(1,int(anmtNum/30)+1): #for each page from 1 to total page number
        #for pageNum in range(1,5):
            result=get_cninfo_anmt_page(pageNum,dateRange)
            anmtList=result["announcements"]
            #print(pageNum)
            for anmt in anmtList:
                #print(anmt["announcementTitle"])
                anmtType=check(anmt)
                if anmtType:
                    f.add_cont( anmt["secCode"] +"_"+
                           anmt["secName"] +"_"+ anmt["announcementTitle"])
                    f.add_body("--------" + anmt["secCode"] +"_"+
                           anmt["secName"] +"_"+ anmt["announcementTitle"]+
                           "_"+datetime.strftime(datetime.fromtimestamp(anmt["announcementTime"]/1000),'%Y-%m-%d')+
                           '_'+str(anmt["announcementTime"]))
                    #pdb.set_trace()
                    report_url=get_HX_anmt_url(anmt)                
                    if report_url:
                        f.add_cont(report_url+'\n')
                        f.add_body(report_url+'\n')
                        anmt_summary=get_anmt_summary(report_url,anmtType)
                        #anmt_summary=get_anmt_content(report_url)
                        #pdb.set_trace()
                        if anmt_summary:
                            pass
                            f.add_body(get_summaryTitle(anmtType))
                            f.add_body(anmt_summary)
                        else:
                            f.add_cont('-------未找到此报告概要!-------')
                            f.add_body('-------未找到此报告概要!-------')
                    else:
                        f.add_cont('-------在和讯网未找到此公告!-------')
                        f.add_body('-------在和讯网未找到此公告!-------')
        f.output()
        f.close()
    else:
        #调试时使用
        anmttest={
            'announcementTime': 1471622400000, 
            'announcementTitle': '非公开发行A股股票预案',
            'secCode': '002662' }
        report_url=get_HX_anmt_url(anmttest)
        if report_url:
            print(report_url)
            anmt_summary=get_anmt_summary(report_url)
            #anmt_summary=get_anmt_content(report_url)
            if anmt_summary:
                pass
                print(anmt_summary)
            else:
                print('-------Have Not Got Report Summary from Fulltext!-------')
        else:
            print('-------Annoucment URL Not Found in Hexun.com!-------')


