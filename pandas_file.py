import pandas as pd

df = pd.read_csv(r"c:\Users\VIVIDCOMMS\Downloads\wps_download\population.csv")
# filtering columns and rows

#print(df) ALL THE RESULT
#print(df['Rank']) SEE RESULT BASE ON

#print(df[df['Rank'] < 13])
#print(df['Country'][df['Rank'] < 13])#return country
#print(df[['Country','Rank']][df['Rank'] < 13])# based on what you want return

#print(df.sort_values(by='Rank', ascending= False)) # this will print descending order
#print(df.sort_values(by='Rank')) #based on ascending
# returning not all the columns

sort = df.sort_values(by=['Rank'], ascending=True)
#print(sort[['Rank', 'Country']]) return based on two columns

print(sort[['Rank', 'Country']][df['Rank'] < 13])


#to convert python file to executed file

#1. pip install auto- py-to-exe
#2. auto-py-exe





