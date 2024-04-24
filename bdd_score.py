import sqlite3

def initialiser_base_de_donnees():
    conn = sqlite3.connect('scores.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS scores
                      (id INTEGER PRIMARY KEY, joueur TEXT, score INTEGER, date_heure DATETIME)''')
    conn.commit()
    conn.close()

def ajouter_score(joueur, score, date_heure):
    conn = sqlite3.connect('scores.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO scores (joueur, score, date_heure) VALUES (?, ?, ?)''', (joueur, score, date_heure))
    conn.commit()
    conn.close()

def meilleurs_scores(nombre):
    conn = sqlite3.connect('scores.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT joueur, score FROM scores ORDER BY score DESC LIMIT ?''', (nombre,))
    meilleurs_scores = cursor.fetchall()
    conn.close()
    return meilleurs_scores

