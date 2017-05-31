from random import randint


def rand_pic_string(request):
    return {'rand_pic_string': '?' + str(randint(0, 100000000))}
