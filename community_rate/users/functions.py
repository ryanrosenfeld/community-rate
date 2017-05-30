import os


def upload_prof_pic(file, user):
    out_file = "static/general/img/prof_pics/" + user.username + '.jpg'
    with open(out_file, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    user.has_pic = True
    user.save()
