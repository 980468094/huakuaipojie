
def get_values_by_key(key, json):
    result = []  # 保存找到的所有value值
    # 1.判断json的类型
    if isinstance(json,dict):
        # 2.如果是字典
        # 2.1 判断key是否在字典的keys里面
        if key in json.keys():
            # 2.1.1 在  value=value 添加到result中
            result.append(json.get(key))
        # else:
            # 2.1.2 不在 在字典的values中继续查找（遍历values）
        for value in json.values():
                result+=get_values_by_key(key, value)
    # 3. 如果是列表
    elif isinstance(json,list):
        # 3.1 遍历列表
        for j in json:
            # 3.2 在每个字典对象中继续查找key
            result+=(get_values_by_key(key, j))
    else:
        return []
        # 4.都不是，直接返回
    return result

json={'result':[{'a':'b'},{'a':'b1'},{'a':{'a':'d'}}],'count':22}
print(get_values_by_key('a',json))
