import re

# qvchu=lambda text: text.replace('-latest', '') if re.findall('(.*)-latest', text) else text
# for i in [{'externalName':'aaa-bbb-latest'},{'externalName':'bbb-ccc-latest'}]:
#             for k in [{'name':'aaa-bbb.uisee'},{'name':'bbb-ccc-latest.uisee'}]:
#                 print(qvchu(k['name'].split('.')[0]))
#                 print(qvchu(i['externalName']))

               # if re.findall('(.*)-latest',k['name'].split('.')[0]): #有带-latest
               #          try:
               #             kk=re.findall('(.*)-latest',i['externalName'])[0]
               #             if kk==re.findall('(.*)-latest',k['name'].split('.')[0])[0]:
               #                 print('相同')
               #          except:
               #             i_re=i['externalName'][0]+'-latest'
               #             print(i_re,k['name'].split('.')[0])
               # else:
               #          #print('k not have latest')
               #          try:
               #             i_re=re.findall('(.*)-latest',i['externalName'])[0]
               #             #print(i_re,k['name'].split('.')[0])
               #             if k['name'].split('.')[0] == i_re:
               #                 print('相同')
               #          except:
               #             i_re=k['name'].split('.')[0].replace('-latest','')
               #             print(i_re,k['name'].split('.')[0])
import os
a= os.path.dirname(os.path.abspath(__file__))
print(a)

