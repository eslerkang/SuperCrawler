from flask import Flask, render_template, request, redirect
from naver import get_webtoon_list, get_id_list, get_last_epi, get_finish_list, get_finish_id_list, get_epis
from datetime import date

app = Flask('Never Webtoon')

webtoon_db = {}
date_db = {}
id_db = {}


@app.route('/')
def index():
    existing_webtoon = webtoon_db.get('webtoon')
    date_today = date_db.get('webtoon')
    id_list = id_db.get('webtoon')
    if existing_webtoon:
        webtoon_list = existing_webtoon
    else:
        webtoon_list = get_webtoon_list()
        webtoon_db['webtoon'] = webtoon_list
        date_today = date.today().isoformat()
        date_db['webtoon'] = date_today
        id_list = get_id_list()
        id_db['webtoon'] = id_list
    return render_template(
        'index.html',
        webtoon_list=webtoon_list,
        date_today=date_today,
        mode_name="완결작품",
        mode='/finish'
    )


@app.route('/detail')
def webtoon():
    try:
        id_list = id_db.get('webtoon')
        finish_id_list = id_db.get('finish')
        idx = request.args.get('id')
        if(not idx):
            raise Exception()
        if idx in id_list:
            webtoon_num = id_list.index(idx)
            content = webtoon_db['webtoon'][webtoon_num]
        elif idx in finish_id_list:
            webtoon_num = finish_id_list.index(idx)
            content = webtoon_db['finish'][webtoon_num]
        else:
            raise Exception()

        last_epi = get_last_epi(content)

        epi_list = get_epis(idx, last_epi)
        
        return render_template(
            'detail.html',
            content=content,
            last_epi=last_epi,
            epi_list=epi_list
        )
    except:
        return redirect('/')


@app.route('/update')
def update():
    webtoon_list = get_webtoon_list()
    webtoon_db['webtoon'] = webtoon_list
    webtoon_list = get_finish_list()
    webtoon_db['finish'] = webtoon_list
    date_today = date.today().isoformat()
    date_db['webtoon'] = date_today
    date_db['finish'] = date_today
    id_list = get_id_list()
    id_db['webtoon'] = id_list
    id_list = get_finish_id_list()
    id_db['finish'] = id_list
    return redirect('/')


@app.route('/finish')
def finish():
    existing_webtoon = webtoon_db.get('finish')
    date_today = date_db.get('finish')
    id_list = id_db.get('finish')
    if existing_webtoon:
        webtoon_list = existing_webtoon
    else:
        webtoon_list = get_finish_list()
        webtoon_db['finish'] = webtoon_list
        date_today = date.today().isoformat()
        date_db['finish'] = date_today
        id_list = get_finish_id_list()
        id_db['finish'] = id_list
    return render_template(
        'index.html',
        webtoon_list=webtoon_list,
        date_today=date_today,
        mode_name='연재작품',
        mode='/'
    )


app.run(host='0.0.0.0', port='80')
