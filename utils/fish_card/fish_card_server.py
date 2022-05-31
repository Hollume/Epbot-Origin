import os

from datetime import datetime
from utils import seta_json
from utils.seta_josa import Josa

here = "utils/fish_card"

async def get_data(fish=None, room=None, user=None):
    theme = user.theme
    theme_exist = f"{here}/theme/{theme}".replace('\\', '/')
    theme = seta_json.get_json(f'{theme_exist}/theme.json')

    if f'rank-{fish.rarity}' not in theme.keys():
        layout = theme['default']
    else:
        layout = theme[f'rank-{fish.rarity}']

    time = datetime.today()
    # 기본 변수 생성
    cost = f"{fish.cost():,}"
    length = f"{fish.length:,}"
    average_cost = f"{fish.average_cost:,}"
    average_length = f"{fish.average_length}"
    maintenance_p = f"{room.maintenance:+}"
    fees_p = f"{-1 * (room.fee + room.maintenance):+}"
    fees = f"{fish.fee(user, room) + fish.maintenance(room):+,}"
    bonus_p = f"{room.bonus:+}"
    bonus = f"{fish.bonus(room):+,}"
    time = time.strftime('%Y-%m-%d %H')
    roomname = deEmojify(room.name)
    username = deEmojify(user.name)
    profit = f"{fish.cost() + fish.fee(user, room) + fish.maintenance(room) + fish.bonus(room):,}"

    catching = ''
    for object in layout:
        if 'rarity' in object.keys() and object['rarity'] == fish.rarity:
            catching += Josa().convert(object['text'].format(name=fish.name))
    if catching == '':
        catching += Josa().convert(layout[0]['text'].format(name=fish.name))

    return {
        "rarity":   str(fish.rarity),
        "is_trash": True if str(fish.rarity) == "0" else False,
        "owned":    True if room.owner_id == user.id else False,
        "catching": catching,
        "price":    f"{cost}$",
        "tax":      f"{fees}$ ({maintenance_p if room.owner_id == user.id else fees_p}%)",
        "bonus":    f"{bonus}$ ({bonus_p}%)",
        "money":    f"{profit}$",
        "name":     fish.name,
        "detail":   f"{length}cm\n(평균 {average_length}cm)\n{cost}$\n(평균 {average_cost}$)",
        "place":    f"{time}시에 '{roomname}'에서\n『{username}』"
    }


def deEmojify(inputString):
    result = inputString.encode('euc-kr', 'ignore').decode('euc-kr')
    if result == '':
        return '알 수 없는 이름'
    else:
        return result
