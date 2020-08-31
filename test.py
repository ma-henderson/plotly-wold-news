from collections import defaultdict
list = ['a', 'b', 'a', 'c']
dict= defaultdict(int)
for item in list:
  dict[item] +=1

# for item, count in dict.items():
#   print(item)
#   if item == 'c':
#     dict['b'] += 1
#     del dict[item]  

print(dict)

# loop through, group items, append to del_list items to be deleted
# then loop through del_list and delete items from dict

# string_one = 'The Fox is over there'
# string_two = 'fox'

# print(string_one.lower().find(string_two.lower()))

