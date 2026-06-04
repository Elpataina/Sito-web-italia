import random
from flask import Flask, render_template
#from siciliano import get_random_italian_word, translate_to_sicilian, vocabolario_siciliano

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


def punti():
    punti = 10
    return render_template("main.html", punti=punti)


if __name__ == "__main__":

    app.run(debug=True)