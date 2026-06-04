import random
from deep_translator import GoogleTranslator
from flask import app
import speech_recognition as sr
from googletrans import Translator
from flask import Flask, render_template
from openai import OpenAI



@app.route("/siciliano.html")
def siciliano():
    corretto = ""
    client = OpenAI(api_key="LA_TUA_API_KEY")



    sicilian =[
        "cavaddu",
        "manciari",
        "taliare",
        "amuri",
        "bedda",
        "picciottu",
        "Sicilia",
        "parrari",
        "picciottu",
        "libbru",
        "casa",
        "mari",
        "suli",

    ]

    word = random.choice(sicilian)
    # =========================
    # 1. Trascrizione audio
    # =========================

    audio_file = open("audio.wav", "rb")

    transcription = client.audio.transcriptions.create(
        model="gpt-4o-mini-transcribe",
        file=audio_file,
        language="it"
    )

    testo_italiano = transcription.text

    print("\n=== TESTO ITALIANO ===")
    print(testo_italiano)

    # =========================
    # 2. Traduzione in siciliano
    # =========================

    response = client.responses.create(
        model="gpt-5",
        input=f"""
    Traduci il seguente testo dall'italiano al siciliano.

    Testo:
    {testo_italiano}

    Restituisci solo la traduzione in siciliano.
    """
    )

    testo_siciliano = response.output_text

    print("\n=== TESTO SICILIANO ===")
    print(testo_siciliano)

    if response == word:
        return render_template("siciliano.html", word=word, testo_siciliano=testo_siciliano, correct="CORRETTO!")
    else:
        return render_template("siciliano.html", word=word, testo_siciliano=testo_siciliano, correct="SBAGLIATO!")


if __name__ == "__main__":
    app.run(debug=True)

