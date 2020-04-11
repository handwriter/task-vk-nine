from flask import Flask, render_template, url_for, redirect, request
from datetime import datetime
from auth import *
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
app = Flask(__name__)


vk_session = VkApi(token=TOKEN)
@app.route('/vk_stat/<int:group_id>')
def vk_stat(group_id):
    vk = vk_session.get_api()
    activity = {}
    ages = {}
    cities = []
    for i in vk.stats.get(group_id=group_id, app_id=7403595, extended=True, intervals_count=10):
        if 'activity' in i:
            for j in i['activity']:
                if j in activity:
                    activity[j] += 1
                else:
                    activity[j] = 1
        if i['reach']['reach'] != 0:
            for j in i['reach']['age']:
                if j['value'] not in ages:
                    ages[j['value']] = j['count']
                else:
                    ages[j['value']] += j['count']
            for j in i['reach']['cities']:
                if j['name'] not in cities:
                    cities.append(j['name'])
    return render_template('vk_stat.html', title='Vk Statistics', activity=activity, ages=ages, cities=cities)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')