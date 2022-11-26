# import numpy as np
# import pandas as pd
# import seaborn as sns
# from datetime import datetime
# import matplotlib.pyplot as plt
# from sqlalchemy import create_engine
# import os, sys, pickle, paramiko, fnmatch, glob
# from arith import map_score, map_eligibility
# from clean import rename, func, adder, status, aggr, drop_cols, date_clip


# with open("vdf_col", "rb") as vp:  
#     vdf_col = pickle.load(vp)
    
# with open("ldf_col", "rb") as jp:   
#     ldf_col = pickle.load(jp)


# def readfile(log_index):
#     path = os.getcwd()
#     all_files = glob.glob(os.path.join(path, log_index + "_*.unl"))
#     df = pd.concat((pd.read_csv(f, sep ='|', header = None) for f in all_files), ignore_index = True)

#     return df


# def score_card():
    
#     '''Calculates the credit score of a number in a dataset
#             Parameters:
#                 voucher_df = Voucher dataset over a period of time
#                 loan_df = Loan dataset over a period of time
#                 number = number to calculate credit score for
                
#             Returns:
#                 df_final = final dataset with duplicates Pri_identity dropped 
          
#     '''     
    
    
#     vdf = readfile('vou')
#     ldf = readfile('loan')
    
#     vdf = rename(vdf_col, vdf)
#     ldf = rename(ldf_col, ldf)

#     new_vdf = func(vdf, value=0)
#     new_ldf = func(ldf, value=0)
    
#     vdf_, ldf_ = date_clip(new_vdf, new_ldf)
    
#     ldf_ = status(ldf_)
    
#     vdf_aggr, ldf_aggr = aggr(vdf_, ldf_, new_vdf, new_ldf)
#     vdf_clean, ldf_clean = drop_cols(vdf_aggr, ldf_aggr)
    
#     df_final = map_score(vdf_clean, ldf_clean)
#     df_final = map_eligibility(df_final)

#     #df_final = df_final.drop_duplicates(subset=['Pri_identity'], keep = 'first')


#     return df_final


# '''def main():
#     client = paramiko.SSHClient()
#     client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     client.connect(hostname = '91.109.117.92', port = 22, username='masterpremote', password ='y3Tya$wjsiOuissty3T')

#     path = os.getcwd()
#     path_files = os.listdir(path)
#     sftp = client.open_sftp()
#     for filename in sftp.listdir('cs_files'):
#         if fnmatch.fnmatch(filename, "*.unl") and filename not in path_files:
#             sftp.get("/home/masterpremote/cs_files/" + filename, path + '/' + filename)
    
    
    
#     db = create_engine('postgresql://postgres:Bytesize@localhost:5432/Bytesize')
#     engine = db
#     cnx = db.connect()
#     df = scorecard()
#     name = 'credit_scores'

#     df.head(0).to_sql(name, engine, if_exists='replace',index=False) #drops old table and creates new empty table
#     conn = engine.raw_connection()
#     cur = conn.cursor()
#     output = io.StringIO()
#     df.to_csv(output, sep='\t', header=False, index=False)
#     output.seek(0)
#     contents = output.getvalue()
#     cur.copy_from(output, name, null="")
#     conn.commit()'''

# if __name__ == "__main__":
#     score_card()
# #consider saving as parquet file for easy readability
