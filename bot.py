from telegram.ext import Updater,MessageHandler,Filters
from binance.client import Client
import numpy,os,talib

client=Client(None,None)

token=os.environ['TELEGRAM_TOKEN']

markets=["ETHBTC", "LTCBTC", "BNBBTC", "NEOBTC", "BCCBTC", "GASBTC", "HSRBTC", "MCOBTC", "WTCBTC", "LRCBTC", "QTUMBTC", "YOYOBTC", "OMGBTC", "ZRXBTC", "STRATBTC", "SNGLSBTC", "BQXBTC", "KNCBTC", "FUNBTC", "SNMBTC", "IOTABTC", "LINKBTC", "XVGBTC", "CTRBTC", "SALTBTC", "MDABTC", "MTLBTC", "SUBBTC", "EOSBTC", "SNTBTC", "ETCBTC", "MTHBTC", "ENGBTC", "DNTBTC", "ZECBTC", "BNTBTC", "ASTBTC", "DASHBTC", "OAXBTC", "ICNBTC", "BTGBTC", "EVXBTC", "REQBTC", "VIBBTC", "TRXBTC", "POWRBTC", "ARKBTC", "XRPBTC", "MODBTC", "ENJBTC", "STORJBTC", "VENBTC", "KMDBTC", "RCNBTC", "NULSBTC", "RDNBTC", "XMRBTC", "DLTBTC", "AMBBTC", "BATBTC", "BCPTBTC", "ARNBTC", "GVTBTC", "CDTBTC", "GXSBTC", "POEBTC", "QSPBTC", "BTSBTC", "XZCBTC", "LSKBTC", "TNTBTC", "FUELBTC", "MANABTC", "BCDBTC", "DGDBTC", "ADXBTC", "ADABTC", "PPTBTC", "CMTBTC", "XLMBTC", "CNDBTC", "LENDBTC", "WABIBTC", "TNBBTC", "WAVESBTC", "GTOBTC", "ICXBTC", "OSTBTC", "ELFBTC", "AIONBTC", "NEBLBTC", "BRDBTC", "EDOBTC", "WINGSBTC", "NAVBTC", "LUNBTC", "TRIGBTC", "APPCBTC", "VIBEBTC", "RLCBTC", "INSBTC", "PIVXBTC", "IOSTBTC", "CHATBTC", "STEEMBTC", "NANOBTC", "VIABTC", "BLZBTC", "AEBTC", "RPXBTC", "NCASHBTC", "POABTC"]

def getClose(market,unit):
    candles=numpy.array(client.get_historical_klines(market,unit,"1 day ago"),dtype='float')
    closePrices=candles[:,4]
    return closePrices
   
def getRSI(market,unit):
    closePrices=getClose(market,unit)
    rsi = talib.RSI(closePrices,timeperiod=14)
    rsiIndex=100>rsi[-1]>65
    return rsi[-1],rsiIndex

def rsiAlert(bot,job):
    for market in markets:
        rsi,rsiIndex=getRSI(market,"15m")
        if rsiIndex:
            job.context.message.reply_text("MARKET: "+str(market)+"\t RSI: "+str(rsi))

def time(bot, update,job_queue):
    job=job_queue.run_repeating(rsiAlert,30,context=update)

def main():
    updater=Updater(token)
    dp=updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text,time,pass_job_queue=True))
    updater.start_polling()

if __name__ == '__main__':
    main()