import pandas as pd



df = pd.read_csv("C:/BigData/CSV/01_data.csv")


type(df)

sr = df.Name

type(sr)



# 열 추출

df_Name = df.Name
df_Name = df["Name"]

df_Name_Country = df[["Name", "Country"]]

type(df_Name_Country)    # 두 줄 이상이므로 dataframe



# 행 추출

df_row_0 = df.loc[0]

type(df_row_0)

df_row_0_3 = df.loc[[0, 3]]

type(df_row_0_3)    # 두 줄 이상이므로 dataframe

df_row_2to5 = df.loc[2:5]



# group by

df_Con_group = df.groupby("Country")

df_Con_group    # 아무것도 안나온다 -- 그룹으로 묶인 상태로 있음

df_Con_group["Age"].mean()



# Iris 데이터 확인

df = pd.read_csv("c:/BigData/CSV/iris.csv")
df.head()
df.tail()
