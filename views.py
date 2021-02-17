from django.shortcuts import render
from django.http import JsonResponse

# private include
from fusioncharts.fusioncharts import FusionCharts
from fusioncharts.models import Traffic
from collections import OrderedDict
from datetime import datetime
import operator
import time

# it is a default view.
# please go to the samples folder for others view

#def catalogue(request):
#    return  render(request, 'catalogue.html')

# private code : service usage

SNI = [['blog', ['blog', 'tistory']],
	['cloud', ['aws', 'dropbox', 'cloud', 'd.docs.live', 'uplusbox', 'guzzoni', 'drive.google', 'wdcp', 'onedrive', 'synology', 'itunes']],
	['docs', ['wiki', 'office', 'onenote', 'evernote']],
	['shopping', ['auction', 'akmall', 'interpark', 'gmarket', 'tmon', 'wemakeprice', '11st', 'kyobobook', 'adapi', 'tworld', 'skyscanner', 'shop', 'jinair', 'korail', 'jejuair', 'flyasiana', 'echosting', 'nprotect', 'yessign', 'mesu.apple', 'bank', 'checkout.naver', 'toastoven', 'pay']],	
	['e-mail', ['mail', 'imap', 'pop', 'smtp', 'login.live.com']],
	['game', ['battle.net', 'game', 'play.google', 'playrix', 'gaikai', 'xbox', 'filecdn', 'gaming', 'mobilecrush', 'onestore']],
	['messenger', ['kakao', 'messenger', 'mtalk', 'skype', 'chat', 'weixin', 'talkgadget']],
     ['online community', ['dcinside', 'fmkorea', 'instiz', 'microsoft', 'github']],
	['sns', ['facebook', 'fbc', 'instagram', 'twiter', 'twimg']],
     ['streaming', ['youtube', 'twitch', 'nflx', 'netflix', 'ytimg', 'rmcnmv', 'video', 'live.veta.naver', 'melon', 'ttvnw', 'genie']],
	['portal site', ['gist', 'naver', 'msn', 'pstatic', 'nate', 'bing', 'daum', 'google', 'yahoo', 'ggpht', 'gstatic', 'mozilla', 'donga', 'zum', 'quantserve']],
	['advertising', ['push', 'wns', 'rubiconproject', 'ad', 'criteo', 'sharethrough', 'mman', 'afclknt', 'doubleclick', 'liftoff', 'dable', 'exosrv', 'taboola', 'sunnywork', 'sonobi', 'undertone']]]

sColor = {'blog' : "#96A5FF", 'cloud' : "#3DFF92", 'docs' : "#FFB6C1",
          'shopping' : "#80E12A", 'e-mail' : "#13C7A3", 'game' : "#91D0D2", 'messenger' : "#5A5AFF",
          'online community' : "#FFDC3C", 'sns' : "#FAC87D", 'streaming' : "#CD853F", 'portal site' : "#CD0000", 'advertising' : "#828282"}

countConfig = OrderedDict()
#protoConfig = OrderedDict()
ipConfig = OrderedDict()
portConfig = OrderedDict()
serviceConfig = OrderedDict()

countSource = OrderedDict()
#protoSource = OrderedDict()
ipSource = OrderedDict()
portSource = OrderedDict()
serviceSource = OrderedDict()

numpkts = []
services = OrderedDict()

def init_chart(request):
    
    countConfig["caption"] = "Packet Amount"
    countConfig["subCaption"] = "per 60 seconds"
    countConfig["yaxisname"] = "Number of packet"
    countConfig["xaxisname"] = "Time"
    countConfig["numdisplaysets"] = "30"
    countConfig["theme"] = "fusion"
    
    serviceConfig["caption"] = "Application Traffic Distribution"
    serviceConfig["subCaption"] = "From the beginning of this page"
    serviceConfig["showValues"] = "1"
    serviceConfig["showPercentInTooltip"] = "0"
    serviceConfig["enableMultiSlicing"] = "1"
    serviceConfig["bgColor"] = "#FFFFFF"
    serviceConfig["bgAlpha"] = "50"
    serviceConfig["borderColor"] = "#FFFFFF"
    serviceConfig["theme"] = "fusion"
    
    ipConfig["caption"] = "Top 10 IP Usage"
    ipConfig["yAxisName"] = "Number of packet"
    ipConfig["theme"] = "fusion"
    
    portConfig["caption"] = "Top 10 Port Usage"
    portConfig["yAxisName"] = "Number of packet"
    portConfig["theme"] = "fusion"
    
    #serviceConfig["caption"] = "Application Traffics"
    #serviceConfig["yaxisname"] = "number of session"
    #serviceConfig["aligncaptionwithcanvas"] = "0"
    #serviceConfig["plottooltext"] = "<b>$dataValue</b> les Trafficads received"
    #serviceConfig["theme"] = "fusion"
    
    countSource["chart"] = countConfig
    #protoSource["chart"] = protoConfig
    ipSource["chart"] = ipConfig
    portSource["chart"] = portConfig
    serviceSource["chart"] = serviceConfig
    
    countSource["data"] = []
    #protoSource["data"] = []
    ipSource["data"] = []
    portSource["data"] = []
    serviceSource["data"] = []
    
    numpkts.clear()
    services.clear()
    
    for app in SNI :
        services[app[0]] = 0  
        
    count_chart = FusionCharts("line", "ex1" , "640", "400", "chart-1", "json", countSource)
    service_chart = FusionCharts("pie2d", "ex2" , "640", "400", "chart-2", "json", serviceSource)
    ip_chart = FusionCharts("bar2d", "ex3" , "640", "400", "chart-3", "json", ipSource)
    port_chart = FusionCharts("bar2d", "ex4" , "640", "400", "chart-4", "json", portSource)
    #service_chart = FusionCharts("bar2d", "ex5" , "800", "1200", "chart-5", "json", serviceSource)
    
    charts = {'c1': count_chart.render(), 'c2': service_chart.render(),
                  'c3': ip_chart.render(), 'c4': port_chart.render()}
    return render(request, 'index.html', charts)

def update_data(source, dic, color):
    source["data"] = []

    for key, value in dic.items():
        data = {}
        data["label"] = key
        data["value"] = value
        if bool(color) :
            data["color"] = color[key]
        source["data"].append(data)

def output():
    datasets = OrderedDict()
    datasets["count"] = countSource
    #datasets["proto"] = protoSource
    datasets["ip"] = ipSource
    datasets["port"] = portSource
    datasets["service"] = serviceSource
    
    return datasets

def update_chart(request):
    start_time = int(time.time()) - 15
    end_time = start_time + 10
    #start_time = 1557934240
    #end_time = 1557934248
    traffics = Traffic.objects.filter(unixtime__gte = start_time, unixtime__lt = end_time)
    L = len(traffics)
    
    if L == 0 :
        return JsonResponse(output())
    
    numpkts.append([end_time, L])
    if len(numpkts) == 30 :
        numpkts.pop()

    counts = OrderedDict()
    for ct in numpkts :
        t = datetime.utcfromtimestamp(ct[0]).strftime('%Y-%m-%d %H:%M:%S')
        counts[t] = ct[1]

    """
    protocols_tp = OrderedDict()e-commerce
    for pkt in traffics :
        proto = pkt.protocol
        if proto in protocols_tp :
            protocols_tp[proto] = protocols_tp[proto] + 1
        else :
            protocols_tp[proto] = 1
    
    oth = 0
    protocols = OrderedDict()
    for key, value in protocols_tp.items():
        if value < L/100 :
            oth = oth + value            
        else :
            protocols[key] = value
    protocols["others"] = oth
    """    
    
    ips = OrderedDict()
    
    for pkt in traffics :
        sip = pkt.src_ip
        dip = pkt.dst_ip
        if sip in ips :
            ips[sip] = ips[sip] + 1
        else :
            ips[sip] = 1
        if dip in ips :
            ips[dip] = ips[dip] + 1
        else :
            ips[dip] = 1

    ips_top10 = sorted(ips.items(), key=operator.itemgetter(1), reverse=True)
    ips = OrderedDict()
    
    for i in range(10) :
        ips[ips_top10[i][0]] = ips_top10[i][1]
            
    ports = OrderedDict()
    
    for pkt in traffics :
        sport = str(pkt.src_port)
        dport = str(pkt.dst_port)
        if sport in ports :
            ports[sport] = ports[sport] + 1
        else :
            ports[sport] = 1
        if dport in ports :
            ports[dport] = ports[dport] + 1
        else :
            ports[dport] = 1    
    
    ports_top10 = sorted(ports.items(), key=operator.itemgetter(1), reverse=True)
    ports = OrderedDict()
    
    for i in range(10) :
        ports[ports_top10[i][0]] = ports_top10[i][1]       
    
    for pkt in traffics :
        if pkt.sni == ' \'NULL\'':
            continue
        for app in SNI :
            f = 0
            for ptn in app[1] :
                if ptn in pkt.sni :
                    services[app[0]] = services[app[0]] + 1
                    f = 1
                    break
            if f == 1 :
                break
    
    update_data(countSource, counts, {})
    #update_data(protoSource, protocols, {})
    update_data(ipSource, ips, {})
    update_data(portSource, ports, {})
    update_data(serviceSource, services, sColor)
    
    #countSource["data"].append({"label": "1557884588", "value": '{}'.format(len(traffics))})
    #return HttpResponse(request.GET.get('message', None))
    return JsonResponse(output())
  
