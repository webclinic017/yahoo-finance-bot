import market, datetime
import pandas_datareader.data as web
import pandas_ta as ta

class bot:

  def __init__(self,type,start_date):

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
            pass
        return daylys

    def indicate():
        analyses = []
        x = self.daylys
        for i in x :
            df = i
            buy = []
            sell = []
            df = df.drop_duplicates()
            df.ta.strategy(["rsi","adosc"],append=True)
            row_iterator = df.iterrows()
            j = 0
            for  i, row in row_iterator:
                if j < (len(df)-1) :
                    if row['Close'] - df['Close'][j+1]  > 0 :
                        buy.append(0)
                        sell.append(1)
                    if row['Close'] - df['Close'][j+1]  < 0 :
                        buy.append(0)
                        sell.append(1)
                j += 1
            print(df.head)
            df["buy"]=buy
            df["sell"]=sell
            analyses.append(df)
        return analyses


    self.start_date = start_date
    self.market = market.market(type)
    self.symbols = self.market.symbols
    self.daylys = save_data()
    self.analyse = indicate()


if __name__ == "__main__" :
    Bot = bot('nasdaq',datetime.datetime(2016, 1, 1))
