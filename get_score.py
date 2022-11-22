# read in dataframe using zip files and concat
import sys
import pandas as pd
from scorecard import score_card


def get_score_and_eligibility(number):
    print(number)
    """
    Input:
        number: Phone number of user

    Returns:
        score: returns the credit score of the phone number
        elm: eligible loan amount of the phone number
    """

    """final_df = pd.read_csv('FDF.csv')
    
    
    if number not in final_df['Pri_identity'].unique().tolist():
        score, eligible_loan = 0, 0
        return 'The user {} has no credit history, hence a credit_score of {} and is eligible for {}'.format(number, score, eligible_loan)
        
    else:
        score = round(final_df[final_df['Pri_identity'] == number].tail(1).Credit_score.values[0], 2)
        eligible_loan = final_df[final_df['Pri_identity'] == number].tail(1).Eligible_Loan_Amt.values[0]
        fdf = final_df[final_df['Pri_identity'] == number]
        return 'The user {} has a credit score of {} and is eligible for {}'.format(number, score, eligible_loan)"""

    df = pd.read_csv("FDS.csv")  # dummy dataset with variables
    df["Pri_identity"] = df["Pri_identity"].astype(str)

    if number not in df["Pri_identity"].unique().tolist():
        credit_score, eligible_loan = 0, 0
        response = {
            "eligible": False,
            "data": {
                "message":f"The user {number} does not exist in the database"
            },
        }

        print(credit_score, eligible_loan)

        return response

        # return 'The user {} has no credit history, hence a credit_score of {} and is eligible for {}'.format(number, credit_score, eligible_loan)

    else:
        credit_score, eligible_loan = (
            round(
                df[df["Pri_identity"] == number]
                .tail(1)[["Credit_score", "Eligible_Loan_Amt"]]
                .iloc[0][0],
                2,
            ),
            df[df["Pri_identity"] == number]
            .tail(1)[["Credit_score", "Eligible_Loan_Amt"]]
            .iloc[0][1],
        )

        response = {
            "eligible": True,
            "data": {
                "number": number,
                "credit_score": credit_score,
                "eligible_loan": eligible_loan,
            },
        }

        print(credit_score, eligible_loan)

        return response

        # return 'The user {} has a credit score of {} and is eligible for {}'.format(number, credit_score, eligible_loan)


# print(get_score_and_eligibility(int(sys.argv[1])))

# return get_score_and_eligibility
