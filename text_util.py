#encoding=utf-8
import re

RE_SEN_SPLITER = u"(.+?(\r|\n|。|!|！|\?|？|;|；|……))"

def get_sentences(text):
    if not isinstance(text, (unicode,)): return []
    s = re.sub(RE_SEN_SPLITER, lambda x: x.group(0)+"\t", text)
    return [x.strip() for x in s.split('\t') if x.strip() != '']


if __name__ == "__main__":
    text = u'''在上市之后，京东的股价虽然也有突出的表现，但是也曾在上市第二天险些破发，不过随后，股价一路上涨，至6月12日，创出了29.6美元/股的新高，不过当日股价仍以跌幅6.31%收盘。在随后的价格交易日中，股价出现涨跌轮转的情况，截至6月30日，公司股价收于28.51美元/股，当日涨幅为1.79%。
    虽然京东是迄今为止中国在美上市公司规模最大的IPO，但是华尔街正等待着今年下半年阿里巴巴集团里程碑式的股票发行交易，据信阿里巴巴的募资规模可能高达200亿美元。
    迅雷“新贵上市”'''
    sentences = get_sentences(text)
    for sen in sentences:
        print sen
        print '='*10
