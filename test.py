from pydantic import BaseModel
from datetime import datetime
from typing import List


class User(BaseModel):
    name: str
    email: str
    phone: str = None

class Pass(BaseModel):
    beauty_title: str
    title: str
    other_titles: str = None
    title_connect: str = None
    data_added: datetime
    level_winter: str = None
    level_spring: str = None
    level_summer: str = None
    level_autumn: str = None
    latitude: float
    longitude: float
    height: int


class Image(BaseModel):
    title: str
    url_path: str
    data_added: datetime


class AddPass(BaseModel):
    user: User
    passes: Pass
    images: List[Image]


t = AddPass(user= {'name': 'Osya', 'email': 'string', 'phone': 'string'}, passes= {'beauty_title':
            'string', 'title': 'string', 'other_titles': 'string', 'title_connect': 'string', 'data_added':
            datetime(2022, 6, 21, 17, 53, 51, 444000), 'level_winter': 'string', 'level_spring':
            'string', 'level_summer': 'string', 'level_autumn': 'string', 'latitude': 0.0, 'longitude':
            0.0, 'height': 0}, images= [{'title': 'string1', 'url_path': '\\x737472696e67', 'data_added':
            datetime(2022, 6, 21, 17, 53, 51, 444000)}, {'title': 'string2', 'url_path': '\\x737472696e67', 'data_added':
            datetime(2022, 6, 21, 17, 53, 51, 444000)}])

u = {'user': {}, 'passes': {'beauty_title': 'fgjfdgjdfg', 'title': 'string', 'other_titles': 'string',
    'title_connect': 'string', 'data_added': datetime(2022, 6, 30, 12, 16, 12, 337000),
    'latitude': 0.0, 'longitude': 0.0, 'height': 0}, 'images': [{'title': 'bu', 'url_path': 'tru',
    'data_added': datetime(2022, 6, 30, 12, 16, 12, 337000)}, {'title': 'dru', 'url_path': 'gpu',
    'data_added': datetime(2022, 6, 30, 12, 16, 12, 337000)}]}

images = {'title': 'bu', 'url_path': 'tru',
    'data_added': datetime(2022, 6, 30, 12, 16, 12, 337000)}, {'title': 'dru', 'url_path': 'gpu',
    'data_added': datetime(2022, 6, 30, 12, 16, 12, 337000)}

print(t)
#print(u)

n=0
for obj in t.images:
    print(obj.copy(update=images[n]))
    n += 1


#print(t.images.copy(update=images))
#t.images.copy(update=u.get('images')) for image in t.images)
#print(t.copy(update={'user': t.user.copy(update=u.get('user')), 'passes': t.passes.copy(update=u.get('passes')), 'images': list(tu.copy(update=images[0]) for tu in t.images)}))

print(t.copy(update={'user': t.user.copy(update=u.get('user')), 'passes': t.passes.copy(update=u.get('passes')), 'images': list(tu.copy(update=dict) for tu in t.images for dict in images)[:len()]}))
t.copy(update={'passes': t.passes.copy(update=u.get('passes'))})
#print(u.get('images'))


