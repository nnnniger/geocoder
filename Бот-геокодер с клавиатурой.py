import json
import vk_api
from vk_api import VkUpload
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
from images import check_get_image

with open('package.json', encoding='utf8') as file:
    data = json.load(file)
    LOGIN = data['login']
    PASSWORD = data['password'],
    TOKEN = data['token'],
    ID_SOOB = data['id']


def get_attachments(text, upload):
    res = True
    if check_get_image(text):
        image = "image.jpg"
    else:
        image = "error.png"
        res = False
    attachments = []
    upload_image = upload.photo_messages(photos=image)
    attachments.append(f"photo{upload_image[0]['owner_id']}_{upload_image[0]['id']}")
    return attachments, res


def main():
    vk_session = vk_api.VkApi(
        token=TOKEN)
    longpoll = VkBotLongPoll(vk_session, ID_SOOB)
    upload = VkUpload(vk_session)

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            text = event.obj.message['text']
            vk = vk_session.get_api()
            res = get_attachments(text, upload)
            attachments = res[0]
            if res[1]:
                message = f'Это {text}. Что вы еще хотите увидеть?'
            else:
                message = "Проблемы с поиском местности"
            vk.messages.send(user_id=event.obj.message['from_id'],
                             message=message,
                             random_id=random.randint(0, 2 ** 64),
                             attachment=','.join(attachments))


if __name__ == '__main__':
    main()
