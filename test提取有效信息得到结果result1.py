'''
  Created on 2015-07-10
  @author:Luckyjo
'''
import json

f = open ('send_msg_2015-01.log.2','r')
a = open ('result1.txt','w')

i = 0
res_lines = []
line = f.readline()

try:
    while line:
        if line.endswith(' log_analyze  INFO     {\n'):

            res_dict = {}
            for i in range(6):
                line = f.next()
                items = line.split(':')
                keywords = items[0].strip().strip('\"')
                value = items[1].strip().lstrip('\"').strip('\,').rstrip('\"')
                res_dict[keywords] = value
            res_lines.append(res_dict)
            
        else:
            line = f.next()
except StopIteration:
    print 'Here is end' 
        
json.dump(res_lines, a)

f.close()
a.close()
