# posts = [
#     {'id': 1, 'image': 'file.png', 'author_id': 1},
#     {'id': 2, 'image': 'file.png', 'author_id': 2},
#     {'id': 3, 'image': 'file.png', 'author_id': 2},
#     {'id': 4, 'image': 'file.png', 'author_id': 2},
#     {'id': 5, 'image': 'file.png', 'author_id': 1},
#     {'id': 6, 'image': 'file.png', 'author_id': 3},
# ]
#
# comments = [
#     {'id': 1, 'message': 'text', 'post_id': 1, 'author_id': 1},
#     {'id': 2, 'message': 'text', 'post_id': 2, 'author_id': 1},
#     {'id': 3, 'message': 'text', 'post_id': 2, 'author_id': 1},
#     {'id': 4, 'message': 'text', 'post_id': 3, 'author_id': 1},
#     {'id': 5, 'message': 'text', 'post_id': 3, 'author_id': 1},
# ]
#
#
# # logic here
#
#
# def func(post):
#     post['comments'] = list(filter(lambda comment: post['id'] == comment['post_id'], comments))
#
#     return post
#
#
# print(list(map(func, posts)))
# print('+' * 100)
#
# qposts = []
# for post in posts:
#     post['comments'] = []
#     for comment in comments:
#         if post.get('id') == comment.get('post_id'):
#             post['comments'].append(comment)
#     qposts.append(post)
#
# print(qposts)

users = [
    {'id': 1, 'username': 'Fazliddin'},
    {'id': 2, 'username': 'Usmon'},
    {'id': 3, 'username': 'Beknur'},
    {'id': 4, 'username': 'Abdulaziz'},
    {'id': 5, 'username': 'Sarvar'},
    {'id': 6, 'username': 'SARDOR'}

]

follow_objects = [
    {'follower': 1, 'following': '3'},
    {'follower': 1, 'following': '6'},
    {'follower': 3, 'following': '6'},
    {'follower': 2, 'following': '6'},
]


user_id = 1
unfollowed_users = []

black_list = []

for user in follow_objects:
    if user['follower'] == user_id:
        black_list.append(int(user['following']))

print(black_list)

res3=[]

black_list3 = list(filter(lambda x: x['id'] != 1 and x['id'] not in black_list, users))
res0 = list(filter(lambda user: user['id'] != 1 and user['id'] not in black_list, users))

print(black_list3)
for user in users:
    if user['id']!=1 and user['id'] not in black_list:
        res3.append(user)

print(res3)



