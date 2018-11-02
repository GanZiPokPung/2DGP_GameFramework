
objects = [[], [], []]

# object layer 로 넣은 obj를 분류하여 그 리스트에 추가함
def add_object(obj, layer):
    objects[layer].append(obj)

# layer를 순회하여 obj를 찾아서 지움
def remove_object(obj):
    for i in range(len(objects)):
        for j in objects[i]:

            if j == obj:
                objects[i].remove(j)
                del j
                return 0

        # if obj in objects[i]:
        #     objects[i].remove(obj)
        #     del obj

# layer를 순회하여 obj들을 모두 지움
def clear():
    for obj in all_objects():
        del obj
    objects.clear()

# 모든 오브젝트들을 순회돌며 yield함
def all_objects():
    for i in range(len(objects)):
        for obj in objects[i]:
            yield obj