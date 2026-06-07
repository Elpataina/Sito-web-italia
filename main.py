import random
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, session
from trascrittore_traduttore import registra_e_trascrivi, traduci_con_gemini

load_dotenv(override=True)

app = Flask("Trascrittore")
app.secret_key = 'secret'

api_key = os.getenv('GEMINI_API_KEY')


proverbi = ["Abbasso l'Inter, viva il Milan",
             "Non è tutto oro quel che luccica, ma il venditore alle bancarelle ti dirà il contrario",
            "L'erba del vicino è sempre più verde, quindi ho preso il tosaerba e sono andato a tagliargliela",
            "Chi nasce tondo non muore quadrato, infatti io sono un ipercubo quadrimensionale",
            "Non ho paura di chi mette l'ananas sulla pizza, ma di chi mette la pizza sull'ananas",
            "I soldi non fanno la felicità, ma la pizza sì: quindi com'è possibile che per comprare la pizza servano i soldi??",
            "Tra i due litiganti il terzo esplode",
            "Chi semina vento viola le leggi della fisica",]


sicilian = {
    "cavaddu": "cavallo",
    "manciari": "mangiare",
    "taliare": "guardare",
    "amuri": "amore",
    "bedda": "bella",
    "picciottu": "ragazzo",
    "parrari": "parlare",
    "libbru": "libro",
    "casa": "casa",
    "mari": "mare",
    "suli": "sole",
}


@app.route("/")
def proverbi_function():
    proverbio = random.choice(proverbi)
    return render_template("main.html", proverb=proverbio)

@app.route("/main")
def punti():
    punti = 10
    return render_template("main.html", punti=punti)


@app.route("/siciliano", methods=["GET", "POST"])
def traduttore():
    if request.method == "GET":
        parola = random.choice(list(sicilian.keys()))
        session['parola_siciliana'] = parola
        session.setdefault('punti', 0)  # inizializza i punti solo se non esistono già
        return render_template("siciliano.html", testo_originale="", testo="", parola_siciliana=parola, risultato="", punti=session['punti'])

    if request.method == "POST":
        testo_italiano = registra_e_trascrivi()
        if not testo_italiano:
            parola = session.get('parola_siciliana', '')
            return render_template("siciliano.html", testo_originale="", testo="Errore: trascrizione non riuscita.", parola_siciliana=parola, risultato="")
        try:
            testo_siciliano = traduci_con_gemini(testo_italiano, "italiano", "siciliano")
        except RuntimeError as e:
            parola = session.get('parola_siciliana', '')
            return render_template("siciliano.html", testo_originale=testo_italiano, testo=str(e), parola_siciliana=parola, risultato="")
        if not testo_siciliano:
            parola = session.get('parola_siciliana', '')
            return render_template("siciliano.html", testo_originale=testo_italiano, testo="traduzione non riuscita.", parola_siciliana=parola, risultato="")
        parola = session.get('parola_siciliana', '')
        return render_template("siciliano.html", testo_originale=testo_italiano, testo=testo_siciliano, parola_siciliana=parola, risultato="")


@app.route("/esercizio", methods=["POST"])
def esercizio_controlla():
    session.setdefault('punti', 0)

    parola_siciliana = session.get('parola_siciliana', '')
    if not parola_siciliana:
        return render_template("siciliano.html", testo_originale="", testo="", parola_siciliana="", risultato="Nessuna parola attiva. Ricarica la pagina.", punti=session['punti'])

    parola_italiana_corretta = sicilian[parola_siciliana]

    risposta_utente = registra_e_trascrivi()
    if not risposta_utente:
        return render_template("siciliano.html", testo_originale="", testo="", parola_siciliana=parola_siciliana, risultato="Trascrizione non riuscita. Riprova!", punti=session['punti'])

    if risposta_utente.strip().lower() == parola_italiana_corretta.strip().lower():
        session['punti'] += 5
        risultato = f"Corretto! '{parola_siciliana}' in italiano è '{parola_italiana_corretta}' (+5 punti)"
    else:
        session['punti'] = max(0, session['punti'] - 2)
        risultato = f"Sbagliato! Hai detto '{risposta_utente}', ma '{parola_siciliana}' in italiano è '{parola_italiana_corretta}' (-2 punti)"

    nuova_parola = random.choice(list(sicilian.keys()))
    session['parola_siciliana'] = nuova_parola

    return render_template("siciliano.html", testo_originale="", testo="", parola_siciliana=nuova_parola, risultato=risultato, punti=session['punti'])


if __name__ == "__main__":
    app.run(debug=True)
