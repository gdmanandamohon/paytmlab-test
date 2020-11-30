import pandas as pd
import numpy as np


def read_df(url):
    return pd.read_csv(url)


#load df
df_dir = 'data/2019/part-0000{0}-890686c0-c142-4c69-a744-dfdc9eca7df4-c000.csv'
dfs = []
for x in range(5):
    td = read_df(df_dir.format(x))
    dfs.append(td)
wt_df = pd.concat(dfs)

'''Now I have the data frames together and filter out the missing values'''

wt_df = wt_df[ (wt_df['TEMP']!=9999.9) |  (wt_df['DEWP']!= 9999.9) | (wt_df['SLP']!=9999.9) |  (wt_df['STP']!= 9999.9)]
wt_df = wt_df[ (wt_df['VISIB']!=999.9) |  (wt_df['WDSP']!= 999.9) | (wt_df['MXSPD']!=999.9) |  (wt_df['GUST']!= 999.9)]    
wt_df = wt_df[ (wt_df['MAX']!=9999.9) | (wt_df['MIN']!= 9999.9) | (wt_df['PRCP']!=99.9) |  (wt_df['SNDP']!= 999.9)]   


#load station and countrylist
st_dir= 'stationlist.csv'
cnt_dir= 'countrylist.csv'  
cnt_df = read_df(cnt_dir)
st_df = read_df(st_dir)



'''here I made a join of 3 different dataframes for merging the data into one data frame and my new dataframe will have  new columns  as country name '''
''' In Haddop platform it's much easier to do, since i don't have that platform facilities, I am moving forward with pandas df'''


finall_df = wt_df.join(st_dir.set_index('STN_NO'), on='STN--- ').join(cnt_df.set_index('COUNTRY_ABBR'), on='COUNTRY_ABBR')

#Here in the table 'finall_df' do have some astetic value '*'  with MIN, didn't get any direction how to handle that. My assumption says that we should just laeave it out and put th real value in thse space.  


''' Let's consider finall_df as table and write SQL for those three question'''
'''   ********   Step 2 - Questions ************* '''

# 1. Which country had the hottest average mean temperature over the year?

SELECT COUNTRY_FULL, max(msx) from 
(
SELECT COUNTRY_FULL, max(avg_TEMP) as msx  from (select COUNTRY_ABBR, avg(TEMP) AS avg_TEMP
      from finall_df
      group by COUNTRY_ABBR)
)

#2. Which country had the most consecutive days of tornadoes/funnel cloud formations?

'''Didn't get the exactly idea based on on which I should determine the tornedo'''


#3. Which country had the second highest average mean wind speed over the year?
SELECT COUNTRY_FULL, max(mxs) AS secon_max_speed

  FROM (SELECT COUNTRY_FULL, max(avg_MXSPD) as msx  from (select COUNTRY_ABBR, avg(MXSPD) AS avg_MXSPD
      from finall_df
      group by COUNTRY_ABBR)

 WHERE msx< max(msx)






