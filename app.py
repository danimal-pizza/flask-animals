from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
DATEIPFAD = 'tiere.txt'


def lade_tiere():
    tiere = []
    try:
        with open(DATEIPFAD, 'r', encoding='utf-8') as f:
            for zeile in f:
                name, rasse = zeile.strip().split(',')
                tiere.append({'name': name, 'rasse': rasse})
    except FileNotFoundError:
        open(DATEIPFAD, 'w').close()  # Lege die Datei an, wenn sie fehlt
    return tiere


def speichere_tiere(tiere):
    with open(DATEIPFAD, 'w', encoding='utf-8') as f:
        for tier in tiere:
            f.write(f"{tier['name']},{tier['rasse']}\n")


@app.route('/')
def index():
    tiere = lade_tiere()
    return render_template('index.html', tiere=tiere)


@app.route('/neu', methods=['GET', 'POST'])
def neu():
    if request.method == 'POST':
        name = request.form['name']
        rasse = request.form['rasse']
        tiere = lade_tiere()
        tiere.append({'name': name, 'rasse': rasse})
        speichere_tiere(tiere)
        return redirect(url_for('index'))
    return render_template('create.html')


@app.route('/bearbeiten/<name>', methods=['GET', 'POST'])
def bearbeiten(name):
    tiere = lade_tiere()
    tier = next((t for t in tiere if t['name'] == name), None)
    if not tier:
        return "Tier nicht gefunden", 404

    if request.method == 'POST':
        tier['name'] = request.form['name']
        tier['rasse'] = request.form['rasse']
        speichere_tiere(tiere)
        return redirect(url_for('index'))

    return render_template('edit.html', tier=tier)


@app.route('/loeschen/<name>', methods=['POST'])
def loeschen(name):
    tiere = lade_tiere()
    tiere = [t for t in tiere if t['name'] != name]
    speichere_tiere(tiere)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
