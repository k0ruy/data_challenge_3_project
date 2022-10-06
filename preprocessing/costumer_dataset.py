# Libraries:
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta


if __name__ == '__main__':
    # import the cleaned dataset:
    df = pd.read_csv(Path('..', 'data', 'online_sales_dataset_cleaned.csv'))

    # create the aggregated costumer dataset:
    df_agg = df.groupby('CustomerId').agg({'Invoice': 'count', 'Quantity': 'sum', 'Price': 'sum',
                                           'Description': ' '.join, 'Country': lambda x: x.value_counts().index[0],
                                           'InvoiceDate': 'max'})
    df_agg.rename(columns={'Invoice': 'NumberOfPurchases', 'Quantity': 'TotalQuantity', 'Price': 'TotalSpent',
                           'InvoiceDate': 'LastPurchase'}, inplace=True)

    # Use the above for our first definition of churn, costumers that have not purchased in the last @timeframe months:
    timeframe = 365
    df_agg['LastPurchase'] = pd.to_datetime(df_agg['LastPurchase'])
    df_agg['CustomerChurned'] = df_agg['LastPurchase'] < datetime(2011, 12, 31) - timedelta(days=timeframe)

    # Delete the variable last purchase as it is a proxy for the target variable:
    # df_agg.drop('LastPurchase', axis=1, inplace=True)

    # check how many churned costumers we have:
    print(f'Number of churned costumers: {df_agg["CustomerChurned"].sum()}')

    # check the number of customers:
    print(f'Number of customers: {df_agg.shape[0]}')

    # save the dataset:
    df_agg.to_csv(Path('..', 'data', 'online_sales_dataset_agg.csv'))

    # save the churned costumers in a separate dataset:
    df_agg[df_agg['CustomerChurned']]['CustomerChurned'].to_csv(Path('..', 'data',
                                                                     'online_sales_dataset_agg_churned.csv'))