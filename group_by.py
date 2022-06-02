import pandas as pd  # Data Wrangling


df = pd.read_csv("pga_tour_data.csv")
df = df.iloc[:, 1:]
df1 = df.groupby('NAME')[['ROUNDS', 'DRIVE_DISTANCE', 'PAR OR BETTER', 'MISSED GIR', 'US_OPEN_TOP_10', 'POINTS',
                         'TOP 10', '1ST']].sum()
print(df1)
df2 = df.groupby(['NAME'])[['SCORING', 'FWY_%', 'GIR_%', 'SG_P', 'SG_TTG', 'SG_T', 'SCRAMBLING_P']].agg(tuple).\
    applymap(list).reset_index()
print(df2)

# df3 = df2.SCORING.apply(pd.Series)
df2[['SCORING1','SCORING2', 'SCORING3', 'SCORING4', 'SCORING5']] = pd.DataFrame(df2.SCORING.tolist(), index=df2.index)
df2[['FWY_%1','FWY_%2', 'FWY_%3', 'FWY_%4', 'FWY_%5']] = pd.DataFrame(df2['FWY_%'].tolist(), index= df2.index)
df2[['GIR_%1','GIR_%2', 'GIR_%3', 'GIR_%4', 'GIR_%5']] = pd.DataFrame(df2['GIR_%'].tolist(), index= df2.index)
df2[['SG_P1','SG_P2', 'SG_P3', 'SG_P4', 'SG_P5']] = pd.DataFrame(df2['SG_P'].tolist(), index= df2.index)
df2[['SG_TTG1','SG_TTG2', 'SG_TTG3', 'SG_TTG4', 'SG_TTG5']] = pd.DataFrame(df2['SG_TTG'].tolist(), index= df2.index)
df2[['SG_T1','SG_T2', 'SG_T3', 'SG_T4', 'SG_T5']] = pd.DataFrame(df2['SG_T'].tolist(), index= df2.index)
df2[['SCRAMBLING_P1','SCRAMBLING_P2', 'SCRAMBLING_P3', 'SCRAMBLING_P4', 'SCRAMBLING_P5']] = pd.DataFrame(
    df2['SCRAMBLING_P'].tolist(), index=df2.index)
df2 = df2.drop(columns=['SCORING', 'FWY_%', 'GIR_%', 'SG_P', 'SG_TTG', 'SG_T', 'SCRAMBLING_P'])
print(df2)

df_total = pd.merge(df1, df2, how='outer', on='NAME')
print(df_total)
df_total.to_csv("final_tour_data.csv")
