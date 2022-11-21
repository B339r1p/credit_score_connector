import pandas as pd

def get_sc(var, a, b, c):
  
  '''
  Input: var, a, b, c
  - var is the variable used to determine the credit score and is gotten from a user's previous recharge and loan history
    var could be the average recharge frequency, frequency of recharge etc
  - a, b and c are ranges for each of the available fatures
  
  Returns: score - this is the score assigned to a user based on his profile for a particular feature.
  performs comparison between a variable and different integer values
  '''

  if var >= a:
    score = 10
  elif b <= var < a:
    score = 7
  elif c <= var < b:
    score = 5
  else:
    score = 3
  
  return score


def get_var_fdf(fvdf, fldf, number):
  '''
    Input:
      fvdf: This is the voucher recharge dataframe
      fldf: This is the loan recharge dataframe
      number: Phone number of user for which the credit score is to be evaluated

      Performs analysis on a dataframe and its series and returns
      a set of variables for further analysis

      Returns:
        months: number of months a user has been last active
        debt: how much a user owes
        avg_rech_per_months: average number of recharge a user has per month
        total_recharge: total recharge a user made over the dataset timeframe
        freq_recharge: the frequency of recharge of the user
        avg_Loan_amt: the average amount of Loan a user has collected
        avg_repay_amt: the average amount of repayment a user has made
        avg_freq_repay: how often the user repays their debt
  '''

  df = fvdf.merge(fldf, on = 'Pri_identity', how = 'outer')
  cdf = df[df['Pri_identity'] == number]
  total_recharge = sum(cdf['Recharge_amt'])
  avg_rech = total_recharge/len(fvdf[fvdf['Pri_identity'] == number])
  ##bal_change = sum(cdf['Chg_Balance'])
  freq_recharge = len(cdf)
  first_rech_day = min(cdf['Entry_date'])
  last_rech_day = max(cdf['Entry_date'])
  last_rech_days = (pd.to_datetime('today').day - last_rech_day.day)
  months = (last_rech_day - first_rech_day).days/30
  if months == 0:
    months = months + 1
  else:
    months = months
  avg_rechfreq_per_month = freq_recharge/months
  avg_rech_per_month = total_recharge/months
  avg_repay_amt = cdf['Repay_amt'].mean()
  avg_Loan_amt = cdf['Loan_amt'].mean()  
  debt = cdf[cdf['Oper_type'] == 'L'].tail(1)['Loan_amt'].values
  repaid = sum(cdf['Repay_amt'])
  freq_col = len(cdf[cdf['Oper_type'] == 'L'])
  freq_repay = len(cdf[cdf['Oper_type'] == 'R'])
  avg_freq_repay = cdf['Repay_amt'].mean()
  
  return months, debt, avg_rech_per_month, total_recharge, freq_recharge, avg_Loan_amt, avg_repay_amt, avg_freq_repay

def get_var_ldf(fvdf, number):
  '''
    Input:
      fvdf: This is the voucher recharge dataframe
      number: Phone number of user for which the credit score is to be evaluated

  
    Performs analysis on a dataframe and its series and returns
    a set of variables for further analysis

      Returns:
        months: number of months a user has been last active
        debt: how much a user owes
        avg_rech_per_months: average number of recharge a user has per month
        total_recharge: total recharge a user made over the dataset timeframe
        freq_recharge: the frequency of recharge of the user
  '''
  
  df = fvdf
  cdf = df[df['Pri_identity'] == number]
  total_recharge = sum(cdf['Recharge_amt'])
  avg_rech = total_recharge/len(fvdf[fvdf['Pri_identity'] == number])
  ##bal_change = sum(cdf['Chg_Balance'])
  freq_recharge = len(cdf)
  first_rech_day = min(cdf['Entry_date'])
  last_rech_day = max(cdf['Entry_date'])
  last_rech_days = (pd.to_datetime('today').day - last_rech_day.day)
  months = (last_rech_day - first_rech_day).days/30
  if months == 0:
    months = months + 1
  else:
    months = months
  avg_rechfreq_per_month = freq_recharge/months
  avg_rech_per_month = total_recharge/months
  avg_Loan_amt = cdf['Loan_amount'].mean()

  #debt = cdf[cdf['Oper_type'] == 'L'].tail(1)['Loan_amount'].values() - no debt history for voucher dataframe

  return months, avg_rech_per_month, total_recharge, freq_recharge


def get_score_fdf(fvdf, fldf, num):
  '''
  Input: 
    fdvf: voucher recharge dataframe
    fldf: loan recharge dataframe
    num: phone number of user 
   
  Returns:
    Score: score of user if number is present in both Loan & Recharge history
    
  '''

  months, debt, var1, var2, var3, var4, var5, var6 = get_var_fdf(fvdf, fldf, num)
  
  # var1, var2, var3, var4, var5, var6 = avg_rech_per_month, total_recharge, freq_recharge, avg_Loan_amt, avg_repay_amt, avg_freq_repay
  
  if months < 3 or var2 < 500 or var3/months < 3 or debt == 0:
    sc = 0

  else:
    sc1 = get_sc(var1, 5000, 2000, 1000)
    sc2 = get_sc(var2, 50000, 20000, 10000)
    sc3 = get_sc(var3, 20, 12, 7)
    sc4 = get_sc(var4, 1000, 500, 200)
    sc5 = get_sc(var5, 1000, 500, 200)
    sc6 = get_sc(var6, 10, 7, 5)

    sc = (sc1 + sc2 + sc3 + sc4 + sc5 + sc6)/6

  return sc

def get_score_vdf(fvdf, num):
  '''Returns the score of user if number is only present in Recharge history'''

  
  months, v1, v2, v3 = get_var_ldf(fvdf, num)
  
  #v1, v2, v3 = avg_rech_per_month, total_recharge, freq_recharge
  if months < 3 or v1 < 500 or v3/months < 3:
    sc = 0

  else:
    sc1 = get_sc(v1, 5000, 2000, 1000)
    sc2 = get_sc(v2, 50000, 20000, 10000)
    sc3 = get_sc(v3, 20, 12, 7)

    sc = (sc1 + sc2 + sc3)/3

  return sc

def scorecard(fvdf, fldf, number):
      '''
      Returns the final score of a user using the number

          Parameters:
            number(int): phone number of user to look up in conventional format

          Returns:
            fsc(int): generated final score of a user
      '''
      if number in fldf['Pri_identity'].unique() and number in fvdf['Pri_identity'].unique():
        fsc = get_score_fdf(fvdf, fldf, number)

      elif number in fvdf['Pri_identity'].unique() and number not in fldf['Pri_identity'].unique():
        fsc = get_score_vdf(fvdf, number)  

      else:
        fsc = 0

      return fsc

def map_score(fvdf, fldf):
    #map scores to Pri_identity in the dataframe
    final_df = fvdf.merge(fldf, on = 'Pri_identity', how = 'outer')


    nums = set(final_df.Pri_identity)
    num_sc = {}

    for i in nums:
      score = scorecard(fvdf, fldf, i)
      num_sc[i] = score

    final_df['Credit_score'] = final_df['Pri_identity'].map(num_sc)
    
    return final_df


def map_eligibility(final_df):
    ''' maps credit scores of users to the available eligible loan amount
    Input:
      final_df: the resulting dataframe after analysis and evaluation
      
    Output:
      final_df: the resulting dataframe with the eligible loan amount included
      
       '''
  
    d = {range(0, 1):0, range(1, 4): 100, range(4, 7): 200, range(7, 9): 500, range(9, 10):1000} 

    final_df['Eligible_Loan_Amt'] = final_df['Credit_score'].astype(int).apply(lambda x: next((v for k, v in d.items() if x in k), 0))
    final_df = final_df.drop_duplicates(subset=['Pri_identity'], keep = 'first')
    
    final_df.to_csv('Final_DF.csv', index = False)
    
    return final_df

