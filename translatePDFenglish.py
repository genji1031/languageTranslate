from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams, LTTextBox, LTTextBoxHorizontal, LTTextLine, LTPage, LTImage, LTFigure
import hashlib, requests
import urllib
import random, time

# 百度的appid  secretKey
appid = '20191220000368093'  # 填写你的appid
secretKey = '0NBx5qcmUsOMQT9O7hET'  # 填写你的密钥
# 写入你的文件名字
fileName = "演示.pdf"

"""
Defined a method through baidu API to excute translate work
Paramters means:
           queryPram : 请求翻译的字符串
           fromLang  : 原文语种
           zh        : 翻译后的语种
"""
def through_baiduapi_to_translate(queryPram, fromLang, toLang):
    myurl = '/api/trans/vip/translate'
    # 随机salt
    salt = random.randint(32768, 65536)
    q = queryPram
    sign = appid + q + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    # 按照百度api接口调用规范定义url
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(salt) + '&sign=' + sign
    # 请求百度a'pi
    rp = requests.get("http://api.fanyi.baidu.com/api/trans/vip/translate" + myurl)
    # 得到结果转json
    print(rp.text)
    trans_result = rp.json()['trans_result']
    content = ""
    # 将所有的翻译结果 进行拼接
    for i in trans_result:
        content += i["dst"]
    print(content)
    return content


# 打开pdf
fp = open(fileName, 'rb')
# 用文件对象创建一个PDF文档分析器
parser = PDFParser(fp)
# 创建一个PDF文档
doc = PDFDocument()
# 连接分析器，与文档对象
parser.set_document(doc)
doc.set_parser(parser)

# 创建PDF，资源管理器，来共享资源
rsrcmgr = PDFResourceManager()
laparams = LAParams()
device = PDFPageAggregator(rsrcmgr, laparams=laparams)
interpreter = PDFPageInterpreter(rsrcmgr, device)
for index, page in enumerate(doc.get_pages()):
    interpreter.process_page(page)
    # 接受该页面的LTPage对象
    layout = device.get_result()
    # 打开一个doc文档
    o = open("resultFile/" + str(index) + ".doc", "bw")
    for x in layout:
        # 如果实例化的对象是LTTextBoxHorizontal
        # 就打印输出内容
        if (isinstance(x, LTTextBoxHorizontal)):
            # 由于百度api限制调用次数所以需要sleep一下
            time.sleep(1)
            content = x.get_text()
            # 替换换行符
            content = content.replace("\n", "")
            # strip后 编码 写入文件
            o.write(through_baiduapi_to_translate(content.strip(), "auto", "zh").encode())
    o.close()


