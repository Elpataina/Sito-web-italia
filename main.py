import random
from flask import Flask, render_template, request
from trascrittore_traduttore import registra_e_trascrivi, traduci_con_gemini, traduci_parole_con_gemini

app = Flask("Trascrittore")

proverbi = ["Abbasso l'Inter, viva il Milan",
             "Non è tutto oro quel che luccica, ma il venditore alle bancarelle ti dirà il contrario",
            "L'erba del vicino è sempre più verde, quindi ho preso il tosaerba e sono andato a tagliargliela",
            "Chi nasce tondo non muore quadrato, infatti io sono un ipercubo quadrimensionale",
            "Non ho paura di chi mette l'ananas sulla pizza, ma di chi mette la pizza sull'ananas",
            "I soldi non fanno la felicità, ma la pizza sì: quindi com'è possibile che per comprare la pizza servano i soldi??",
            "Tra i due litiganti il terzo esplode",
            "Chi semina vento viola le leggi della fisica",]

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

    # Metodo GET: quando l'utente accede alla pagina, viene mostrato il testo tradotto in siciliano (vuoto all'inizio)    
    if request.method == "GET":
        return render_template("siciliano.html", testo="")
    
    
    # Metodo POST: quando l'utente clicca sul pulsante, viene registrato il vocale, trascritto in italiano e tradotto in siciliano, infine viene mostrato il risultato nella pagina siciliano.html 
    if request.method == "POST":
        testo_italiano = registra_e_trascrivi()
        testo_siciliano = traduci_con_gemini(testo_italiano, "italiano", "siciliano")
        return render_template("siciliano.html", testo=testo_siciliano)


@app.route("/siciliano", methods=["GET", "POST"])
def traduttoreparole():

    if request.method =="GET":
        return render_template("siciliano.html", parola="", correct="")
    if request.method == "POST":
        parola_italiana = request.form.get("parola")
        parola_siciliana = traduci_parole_con_gemini(parola_italiana, "italiano", "siciliano", parola_italiana)
        return render_template("siciliano.html", parola=parola_italiana, correct="")

if __name__ == "__main__":

    app.run(debug=True)