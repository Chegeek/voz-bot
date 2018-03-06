from telegram.ext import Updater,MessageHandler,Filters
from binance.client import Client
import numpy,talib

client=Client(None,None)
token=os.environ['TELEGRAM_TOKEN']

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
    rsi,rsiIndex=getRSI("CNDBTC","15m")
    if rsiIndex:
        job.context.message.reply_text("MARKET: CNDBTC \t RSI: "+str(rsi))

def time(bot, update,job_queue):
    job=job_queue.run_repeating(rsiAlert,30,context=update)

def main():
    updater=Updater(token)
    dp=updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text,time,pass_job_queue=True))
    updater.start_polling()

if __name__ == '__main__':
    main()