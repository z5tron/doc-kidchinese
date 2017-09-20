# -*- coding: utf-8 -*-
# Python 2.7

from flask import Flask, current_app
from flask import render_template
from flask import Response, request, jsonify, g

import codecs
import random
import sqlite3
from os import path
from datetime import datetime, timedelta


app = Flask(__name__)

# DBFNAME = path.join(app.root_path, "chinese.sqlite3")
DBFNAME = "/mnt/media/www/apache24/data/db.sqlite3"

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DBFNAME)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()




@app.route('/')
def hello_world():

    T = datetime.now() - timedelta(days=4)
    conn = get_db()
    cur = conn.cursor()
    return current_app.send_static_file("chinese.html")

@app.route('/words')
def getWords():
    conn = get_db() # sqlite3.connect("chinese.sqlite3")
    cur = conn.cursor()
    dt = datetime.now().strftime("%Y-%m-%d")
    ncut = 50
    cur.execute('select wordId,word,points from pool where points < ?', (ncut,))
    d = dict([(r[0], {'wordId': r[0], 'word': r[1], 'points': r[2], 'dateStudy': ''}) for r in cur.fetchall()])
    cur.execute('select wordId,max(dateStudy),sum(points) from progress group by wordId')
    for wordId,dateStudy,points in cur.fetchall():
        if wordId not in d: continue # new word, no progress yet, good candidate
        if dateStudy[:10] == dt: # studied today, skip
            d.pop(wordId)
            continue
        d[wordId]['dateStudy'] = dateStudy
    kn = random.sample(d.keys(), min(20, len(d)))
    for k in kn:
        cur.execute('select w.wordId,b.bookName from wordbook as w left join books as b on w.bookId=b.bookId where w.wordId=?',
                    (d[k]['wordId'],))
        d[k]['books'] =','.join([c[1].strip() for c in cur.fetchall()])

    return jsonify({'words': [d[k] for k in kn], 'cut': ncut, 'totalWords': len(d)})


@app.route('/save', methods=['POST'])
def saveWords():
    words = request.get_json()
    # return Response("{}".format(words), mimetype="text/text")
    conn = get_db() # sqlite3.connect("chinese.sqlite3")
    cur = conn.cursor()
    saved = []
    for word in words:
        if word.get('skip', 0): continue
        cur.execute('update pool set points=points + ? where wordId=?',
                    (word['score'], word['wordId']))
        cur.execute('insert into progress(wordId, points, dateStudy) values(?,?,?)',
                    (word['wordId'], word['score'], word['dateStudy']))
        saved.append(word)
    if saved:
        conn.commit()
    #return Response("{}\n{}".format(words, saved), mimetype="text/text")
    return jsonify(saved)


@app.route('/review/<deadline>')
def review_words(deadline):
    deadline = ''.join(x for x in deadline if x.isdigit())
    T = datetime.now() + timedelta(days=1)
    dt1 = "{}-{}-{}".format(deadline[:4], deadline[4:6], deadline[6:8]) #T.strftime("%Y-%m-%d")
    dt2 = T.strftime("%Y-%m-%d")
    if len(deadline) >= 16:
        dt2 =  "{}-{}-{}".format(deadline[8:12], deadline[12:14], deadline[14:16])
    conn = get_db()
    cur = conn.cursor()

    cur.execute('select prog.wordId,pool.word,prog.dateStudy,pool.points from (select * from progress where points < 0) as prog left join pool on prog.wordId=pool.wordId where prog.dateStudy > ? and prog.dateStudy < ? and pool.points < 50 ORDER by prog.dateStudy ASC', (dt1, dt2,))
    words = [{'wordId': r[0], 'word': r[1], 'dateStudy': r[2], 'points': r[3]} for r in cur.fetchall()]
    
    return render_template("chinese_review.html", words=words)



