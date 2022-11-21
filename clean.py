import pandas as pd
#rename duplicate column names and asiign new column names

def rename(col_list, df):
    '''
    Input:
        col_list: list of columns for renaming the dataframe
        df: dataframe of which the columns are to be renamed
        
    Output:
        df: resulting dataframe after the columns have been renamed'''
    
    dup = list(set([x for x in col_list if col_list.count(x) > 1]))

    cols = []
    col = []
    count = 1
    for i in col_list:
        if i in dup:
          p = col.count(i) + 1
          cols.append(i+ str(p))
          col.append(i)
        else:
          cols.append(i)

    df.columns = cols
    
    return df


#replace NaN values with 0
def func(df, value):
  '''replaces NaN values in a dataframe with desired value'''
  df = df.copy()
  for col in df:
      # select only integer or float dtypes
      if df[col].dtype in ("int", "float"):
          df[col] = df[col].fillna(value)
  return df


def adder(df,ln, col_diff,col_num, col_name = 'col_n'):
  '''
  Returns the aggregated sum of columns with the same userID

  Parameters:
      df = dataframe
      ln = length of the group of columns to aggregate
      col_diff = length of difference between columns to aggregate
      col_num = column number
      col_name(optional) = column name

  returns
     Dateframe of aggregated columns
  '''

  ndf = pd.DataFrame() #create an empty dataframe
  for i in range(ln):
    num = col_num + (col_diff*i)
    col = 'col' + str(i)
    ndf[col] = df.iloc[:, num]    #append all columns to aggregate to the empty dataframe
  
  ndf['col_n'] = ndf.sum(axis=1, numeric_only= True)  #sum all the columns added
  return ndf['col_n']


def date_clip(vdf_, ldf_):
    #clean and convert date columns to datetime 
    ldf_['Oper_date'] = ldf_['Oper_date'].astype(str).str[:8]
    ldf_['Entry_date'] = ldf_['Entry_date'].astype(str).str[:8]
    vdf_['Entry_date'] = vdf_['Entry_date'].astype(str).str[:8]
    vdf_['Starttimeofbillcycle'] = vdf_['Starttimeofbillcycle'].astype(str).str[:8]

    vdf_cols = ['Entry_date', 'Starttimeofbillcycle']
    ldf_cols = ['Oper_date', 'Entry_date']
    
    
    ldf_[ldf_cols] = ldf_[ldf_cols].apply(pd.to_datetime, format='%Y%m%d')
    vdf_[vdf_cols] = vdf_[vdf_cols].apply(pd.to_datetime, format='%Y%m%d')
    
    return vdf_, ldf_


def status(ldf):
    #To create Loan Status column
    
    nums = set(ldf.Pri_identity)
    num_dic = {}

    for i in nums:
      ldf_ = ldf.sort_values('Oper_date')
      debt = ldf_[ldf_['Pri_identity'] == i].tail(1)['Loan_amt']

      if int(debt) > 0:
        status = 1
      else:
        status = 0

      num_dic[i] = status
    
    #where 0 means debt cleared and 1 means still owing...
    ldf_['Loan_status'] = ldf_['Pri_identity'].map(num_dic)
    
    return ldf_


def aggr(vdf_, ldf_, new_vdf, new_ldf):
    #get aggregate for the columns for Balance Change Information
    vdf_['BC_Cur_balance'] = adder(new_vdf, 10,  5, 67)
    vdf_['BC_Chg_balance'] = adder(new_vdf, 10, 5, 68)

    #get aggregate for the columns for Free Unit Change Information
    vdf_['FU_Cur_amount'] = adder(new_vdf, 10,  7, 118)
    vdf_['FU_Chg_amount'] = adder(new_vdf, 10, 7, 119)

    #get aggregate for the columns for Bonus Details
    vdf_['Bonus_amount'] = adder(new_vdf, 10, 6, 187)
    vdf_['Bonus_Cur_balance'] = adder(new_vdf, 10,  6, 188)

    #get aggregate for the columns for Free Reward Details
    vdf_['FR_Bonus_Amount'] = adder(new_vdf, 10, 8, 248)
    vdf_['FR_Cur_amount'] = adder(new_vdf, 10,  8, 249)


    #get aggregate for change information
    ldf_['Cur_Balance'] = adder(new_ldf, 5, 3, 19)
    ldf_['Chg_Balance'] = adder(new_ldf, 5, 3, 20)
    
    return vdf_, ldf_

def drop_cols(vdf_, ldf_):
    #list of columns to drop in loan df

    drop_ldf = ['Loan_balance_type', 'Trans_id','Pri_offering', 'Entry_date', 'Sub_id', 'Sequenceid', 'Bill_cycle_id', 'Init_etu_amt', 
                'Etu_amt','Etu_grace_date', 'Force_repay_date','Reserved1', 'Reserved2', 'Reserved3', 'Reserved4', 'Reserved5','Reserved6', 
                'Reserved7', 'Reserved8', 'Reserved9', 'Reserved10','Reserved11']
    
    

    #list of columns to drop in the vou df

    #drop card_details
    drop_vdf = ['Recharge_log_id', 'Acct_id1', 'Sub_id','Third_party_number','Currency_rate', 
                'Currency_id','Conversion_amt','Ext_trans_type','Recharge_trans_id', 'Batch_no', 'Recharge_tax', 'Recharge_penalty', 
                'Recharge_reason','Result_code', 'Error_type', 'Diameter_sessionid', 'Oper_id', 'Dept_id', 'Recon_date', 'Recon_status',
                'Reversal_trans_id', 'Reversal_reason_code', 'Reversal_oper_id', 'Reversal_dept_id', 'Reversal_date', 'Ext_trans_id',
                'Card_sequence', 'Card_pin_number', 'Card_batch_no', 'Card_status', 'Card_cos_id', 'Card_sp_id', 'Card_amount', 
                'Card_validity', 'Voucher_encrypt_number', 'Check_no', 'Check_date', 'Credit_card_no', 'Credit_card_name',
                'Credit_card_type_ID', 'Cc_expiry_date', 'Cc_authorization_code', 'Bank_code', 'Bank_branch_code', 'Acct_no',
                'Bank_acct_name', 'Reserved1','Reserved2','Reserved3','Reserved4','Reserved5','Reserved6','Reserved7',
                'Reserved8','Reserved9','Reserved10','Reserved11','Reserved12','Reserved13','Reserved14','Reserved15','Reserved16',
                'Reserved17','Reserved18','Reserved19','Reserved20','Reserved21','Reserved22','Reserved23',
                'Reserved24','Reserved25','Reserved26','Reserved27','Reserved28','Reserved29','Reserved30','Reserved31','Reserved32',
                'Reserved33','Reserved34','Reserved35','Reserved36','Reserved37','Reserved38', 'Suspendstop', 'Region_code', 'Be_code', 
                'Remark', 'Previousactivestop','Be_id', 'Rechargeareacode', 'Istestnumber',
                'Newactivestop']
    
    
    #drop off columns
    vdf_clean = vdf_.drop(columns = drop_vdf).drop(vdf_.iloc[:, 65:325], axis = 1)
    ldf_clean = ldf_.drop(columns = drop_ldf).drop(ldf_.iloc[:, 18:33], axis = 1)
    
    #convert columns to Naira
    vdf_cols = ['BC_Cur_balance', 'BC_Chg_balance', 'FU_Cur_amount', 'FU_Chg_amount', 'Bonus_amount', 'Bonus_Cur_balance', 
                'FR_Bonus_Amount', 'FR_Cur_amount', 'Recharge_amt', 'Original_amt', 'Loan_amount', 'Loan_poundate']
    ldf_cols = ['Init_loan_amt', 'Init_loan_poundage', 'Loan_amt', 'Loan_poundage', 'Repay_amt', 'Repay_poundage', 'Cur_Balance', 
                'Chg_Balance']

    vdf_clean[vdf_cols] = vdf_clean[vdf_cols]/100
    ldf_clean[ldf_cols] = ldf_clean[ldf_cols]/100

    #remove outlier from Chg_Balance column
    ldf_clean = ldf_clean[ldf_clean['Chg_Balance'] <= 5000]
    fldf = ldf_clean.copy()
    fvdf = vdf_clean.copy()
    
    
    return fvdf, fldf
