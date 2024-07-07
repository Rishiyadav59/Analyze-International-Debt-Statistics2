import pandas as pd
import os

# Define the folder path
folder_path = "C:/Users/RISHI KUMAR YADAV/Desktop/data_ analyst/data" 



df=pd.read_csv("IDS_ALLCountries_Data.csv",encoding="latin-1") #to read the given data
#to delete last unwanted rows
num_rows = len(df)
df = df.iloc[:num_rows - 5]
df2=pd.read_csv("IDS_CountryMetaData.csv",encoding="latin-1")

df = df.fillna('0')

exclude=["Country Name","Counterpart-Area Name","Counterpart-Area Code","Series Code"] #columns we dont need

for num in range(1970,2018):
   exclude.append(str(num))
for num in range(2023,2031):
    exclude.append(str(num))
df_2000_2022 = df.drop(exclude, axis=1) # taking the columns fron 2000 to 2022

#there is one indector called present value of external stocks, it is the best indector to analysis the debt of countries

present_value_row = df[df.eq('Present value of external debt (current US$)').any(axis=1)]
for num in range(1970,2031):
  if num != 2022:
    exclude.append(str(num))
present_value_of_external_stocks = present_value_row.drop(exclude, axis=1)

# Create the folder if it doesn't exist
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
filepath = os.path.join(folder_path, "present_value_of_external_stock.csv")

present_value_of_external_stocks.to_csv(filepath, index=False)

#list of indectors we will use to analysis
indecators=["Debt service on external debt, total (TDS, current US$)",
   "Debt forgiveness or reduction (current US$)",
   "Total change in external debt stocks (current US$)",
   "Total reserves (includes gold, current US$)",
   "External debt stocks, total (DOD, current US$)"]
indectors_common=pd.DataFrame()
#df_2000_2022["Series Name"]=df_2000_2022["series_name"]
for i in indecators:
    
       present_value_row = df_2000_2022[df.eq(i).any(axis=1)]
       for i in range(2018,2023):
            list1=[2018,2019,2020,2021,2022]
            list1=list1.remove(i)
            date_data=present_value_row.drop(list(str(list1)),axis=1)
            date_data["years"]=i
       indectors_common=date_data.append(present_value_row)




#country metadata data
country_meatdata=df2[["Code","Income Group","Region"]]
#null value treatment
country_meatdata = country_meatdata.rename(columns={'Income Group': 'Income_Group'})
column_to_impute = 'Income_Group'
column_to_impute2 = 'Region'
country_meatdata[column_to_impute] = country_meatdata[column_to_impute].fillna(country_meatdata[column_to_impute].mode()[0])
country_meatdata[column_to_impute2] = country_meatdata[column_to_impute2].fillna(country_meatdata[column_to_impute2].mode()[0])
filepath = os.path.join(folder_path, "country_metadat.csv")
country_meatdata.to_csv(filepath, index=False)

#country name and code
country_name_code=df.iloc[:,:2]
country_name_code=country_name_code.drop_duplicates()
filepath = os.path.join(folder_path, "country_name_code.csv")
country_name_code.to_csv(filepath, index=False)


#principal repayments
indecators1=[
             "Principal repayments on external debt, other public sector (PPG) (AMT, current US$)",
             "Principal repayments on external debt, private guaranteed by public sector (PPG) (AMT, current US$)",
             "Principal repayments on external debt, private nonguaranteed (PNG) (AMT, current US$)",
             "Principal repayments on external debt, public and publicly guaranteed (PPG) (AMT, current US$)",
             "Principal repayments on external debt, public sector (PPG) (AMT, current US$)"]                          


principal_repayments=pd.DataFrame()
for i in indecators1:
    present_value_row = df_2000_2022[df.eq(i).any(axis=1)]
    principal_repayments=principal_repayments.append(present_value_row)

#principal_repayments["total"] = principal_repayments[indecators1].sum(axis=1)
filepath = os.path.join(folder_path, "principal_repayments.csv")
principal_repayments.to_csv(filepath, index=False)