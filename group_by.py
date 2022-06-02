import pandas as pd  # Data Wrangling


df = pd.read_csv("pga_tour_data.csv")
df = df.iloc[:, 1:]
df1 = df.groupby('NAME')[['ROUNDS', 'DRIVE_DISTANCE', 'PAR OR BETTER', 'MISSED GIR', 'US_OPEN_TOP_10', 'POINTS',
                         'TOP 10', '1ST']].sum()
print(df1)
df2 = df.groupby(['NAME'])[['SCORING', 'FWY_%', 'GIR_%', 'SG_P', 'SG_TTG', 'SG_T', 'SCRAMBLING_P']].agg(tuple).\
    applymap(list).reset_index()
print(df2)

df_total = pd.merge(df1, df2, how='outer', on='NAME')
print(df_total)
df_total.to_csv("final_tour_data.csv")
