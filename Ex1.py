import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
df=pd.read_csv('athletes.csv')
df.info()
start=df.head()
end=df.tail()
#print(start,end)
usaPlayers=df[df['nationality']=='USA']
#print(usaPlayars)
womenPlayer=df[df.sex=='female']
#print(womenPlayer)
volleyballSoccer=df[(df.sport=='volleyball') | (df.sport=='football') ]
#print(volleyballSoccer)
speacialPlayers=df[(df.weight>70) &(df.height>1.80)]
#print(speacialPlayers)
df['yob'] =df.dob.apply(lambda x: x.split('/')[2])
#print(df)
df['age']=df.yob.apply(lambda x: 2020 - int(x))
#print(df)
df['got_medal']= (df.bronze + df.silver + df.gold)>0 
#print(df.head(10))
maxAge=df.age.max()
minAge=df.age.min()
avg=df.age.mean()
#print(maxAge,minAge)
#print("the avg is",avg)
avgHeight=df.height.mean()
#print(avgHeight)
howMany=df.sport.value_counts()
#print(howMany.count())
#print(howMany)
#print(df.got_medal.value_counts())
print(df)
sns.barplot(data=df,x=round(df.height, 1),y=df.weight)
plt.show()