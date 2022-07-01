import market, datetime
import pandas_datareader.data as web
import pandas_ta as ta
from math4machinelearning.artificialneuralnetwork import *
from math4machinelearning.artificialneuralnetwork import artificialneuralnetwork_classifier
import pandas as pd
import numpy as np
import argparse

class bot:

  def __init__(self,type="",start_date=datetime.datetime(2021,1,1),symbol=""):

    def save_data():
      daylys = []
      for v in self.symbols :
        start = self.start_date
        end = datetime.date.today()
        try:
            df = web.DataReader(v, "yahoo", start , end)
            daylys.append(df)
            df.to_csv('./data/'+v+'.csv')
        except Exception as e:
            print(e)
            pass
      return daylys

    def learn():
        ANN = {}
        for v in self.symbols :
            df = pd.read_csv('./analyse/'+v+'.csv')
            df = df.dropna(axis=0)
            x = np.matrix(df[["EMA","RSI_14","macd"]].to_numpy() )
            y1 = np.matrix(df[["buy"]].to_numpy())
            y2 = np.matrix(df[["sell"]].to_numpy())
            ann_sell = artificialneuralnetwork_classifier.artificialneuralnetwork_classifier(x,y1)
            ann_buy = artificialneuralnetwork_classifier.artificialneuralnetwork_classifier(x,y2)
            ANN[v] = {
                    "buy" : ann_buy,
                    "sell" : ann_sell
                    }
        return ANN

    def indicate():
        bot_strategie = ta.Strategy(
            name="Bot strat",
            description="Bot strategy",
            ta=[
            {"kind": "ema", "length": 8},
            {"kind": "ema", "length": 21},
            {"kind": "rsi"},
            {"kind": "macd", "fast": 8, "slow": 21, "col_names": ("MACD", "MACD_H", "MACD_S")},
            {"kind": "rsi"},
            ]
            )
        analyses = []
        k = 0
        for s in self.daylys :
            df = s
            buy = []
            sell = []
            df = df.drop_duplicates()
            df.ta.strategy(bot_strategie,append=True)
            row_iterator = df.iterrows()
            j = 0
            for  m, row in row_iterator:
                if j < (len(df)-1) :
                    if row['Close'] - df['Close'][j+1]  > 0 :
                        buy.append(0)
                        sell.append(1)
                    if row['Close'] - df['Close'][j+1]  < 0 :
                        buy.append(1)
                        sell.append(0)
                    if row['Close'] - df['Close'][j+1] == 0 :
                        buy.append(0)
                        sell.append(0)
                if j == (len(df)-1) :
                        buy.append("")
                        sell.append("")
                j += 1
            df["buy"]=buy
            df["sell"]=sell
            df["EMA"]= df["EMA_21"] - df["EMA_8"]
            df["macd"]= df["MACD_H"] - df["MACD_S"]
            analyses.append(df)
            df.to_csv('./analyse/'+self.symbols[k]+'.csv')
            k += 1
        return analyses

    def predict():
        prediction = {}
        for v in self.symbols :
            df = pd.read_csv('./analyse/'+v+'.csv')
            bottom = df.tail(1)
            x = bottom[["EMA","RSI_14","macd"]].to_numpy()
            buy = self.neurones[v]["buy"].predict(x)
            sell = self.neurones[v]["sell"].predict(x)
            prediction[v] = {
                "buy" : buy,
                "sell": sell
            }
            return prediction



    self.start_date = start_date
    if symbol == "" :
        self.market = market.market(type)
        self.symbols = self.market.symbols
    if symbol != ""  :
        self.symbols = [symbol]
    self.daylys = save_data()
    self.analyse = indicate()
    self.neurones = learn()
    self.prediction = predict()


if __name__ == "__main__" :
    parser = argparse.ArgumentParser(description='Yahoo Finance Bot : A tool that predict the dayly tendance of a market (Sell VS Buy) on the basis of Exponential Mooving Average, MACD and RSI.')
    parser.add_argument("-market" , "-m", help=" Precise the market you wish to analayse. This function implement (nasdaq , nyse , world_indice , forex , crypto , mutual_fund, comodities) .")
    parser.add_argument("-value", "-v",help=" Precise a market value to analyse. Exemple : BTC-USD ")
    parser.add_argument("-out", "-o", help=" Precise the file in witch you want to save the result. By default result.txt")
    parser.add_argument("-day", "-d", help=" Start-date : Precise the start day ")
    parser.add_argument("-month", "-mo", help=" Start-date : Precise the start month ")
    parser.add_argument("-year", "-y", help=" Start-date : Precise the start year ")
    args = parser.parse_args()

    if args.market == None :
        print(" No market fill")
    else :
        print("\n-----------------------------\n |"," Market Study : ",args.market,"|\n-----------------------------" )
        if args.day == None :
            print(" You should precise at less a day from wish to start the analyse .")
        if args.month == None :
            print(" You should precise at less a month from wish to start the analyse .")
        if args.year == None :
            print(" You should precise at less a years from wish to start the analyse .")
        else :
            print(" |Start DATE :",args.day,"/", args.month,"/", args.year,"|\n-----------------------------\n" )
            Bot = bot(type=args.market,start_date=datetime.datetime(int(args.year), int(args.month) , int(args.day) ))
            for v in Bot.symbols :
                print("\n-----------------------------\n |"," Value Study : ",v,"|\n-----------------------------\n" )
                print("\n-----------------------------\n |","Bot says buy bit is :", int(Bot.prediction[v]["buy"]),"|\n-----------------------------\n" )
                print("\n-----------------------------\n |","Bot says sell bit is :", int(Bot.prediction[v]["sell"]),"|\n-----------------------------\n" )
                if int(Bot.prediction[v]["buy"]) == 0 and int(Bot.prediction[v]["sell"]) == 1 :
                    print("\n-----------------------------\n |"," You should sell it","|\n-----------------------------\n" )
                if int(Bot.prediction[v]["buy"]) == 1 and int(Bot.prediction[v]["sell"]) == 0 :
                    print("\n------------------------\n |"," You should buy it","|\n------------------------\n" )
                if int(Bot.prediction[v]["buy"]) == 0 and int(Bot.prediction[v]["sell"]) == 0 :
                    print("\n------------------------\n |"," You should wait ","|\n------------------------\n" )
    if args.value == None :
        print(" No value choose ")
    else :
        print("\n-----------------------------\n |"," Value Study : ",args.value,"|\n-----------------------------\n" )
        if args.day == None :
            print(" You should precise at less a day from wish to start the analyse .")
        if args.month == None :
            print(" You should precise at less a month from wish to start the analyse .")
        if args.year == None :
            print(" You should precise at less a years from wish to start the analyse .")
        else :
            print(" |Start DATE :",args.day,"/", args.month,"/", args.year,"|\n-----------------------------\n" )
            Bot = bot(symbol=args.value,start_date= datetime.datetime(int(args.year), int(args.month) , int(args.day) ))
            print("\n-----------------------------\n |","Bot says buy bit is :", int(Bot.prediction[args.value]["buy"]),"|\n-----------------------------\n" )
            print("\n-----------------------------\n |","Bot says sell bit is :", int(Bot.prediction[args.value]["sell"]),"|\n-----------------------------\n" )
            if int(Bot.prediction[args.value]["buy"]) == 0 and int(Bot.prediction[args.value]["sell"]) == 1 :
                print("\n-----------------------------\n |"," You should sell it","|\n-----------------------------\n" )
            if int(Bot.prediction[args.value]["buy"]) == 1 and int(Bot.prediction[args.value]["sell"]) == 0 :
                print("\n------------------------\n |"," You should buy it","|\n------------------------\n" )
            if int(Bot.prediction[args.value]["buy"]) == 0 and int(Bot.prediction[args.value]["sell"]) == 0 :
                print("\n------------------------\n |"," You should wait ","|\n------------------------\n" )
    if args.value == None and args.market == None :
        print(" You should precise at less a value or a market.")
    #Bot = bot('ninja',datetime.datetime(2021, 12, 1))
