# teste 1
import re


text = 'A1 23a'
text = text.lower().replace(' ','')
print(text)

# teste 2

text2 = 'Sustentação - testeando - Q2'
PRIORITY = ['-Q[1,2,3]', '- Q[1,2,3]', ' - Q[1,2,3]']
for Q in range(0, 3):
    text2 = re.sub(PRIORITY[Q], '', text2)
print(text2)