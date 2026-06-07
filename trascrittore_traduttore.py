import os
import sounddevice
import speech_recognition
import scipy.io.wavfile as wav
from google import genai
from google.genai import types
from dotenv import load_dotenv


load_dotenv(override=True)


def registra_e_trascrivi():
    numero_segmenti_al_secondo = 44100
    durata_registrazione=3

    # Registra l'audio
    registrazione = sounddevice.rec(
        frames=(durata_registrazione * numero_segmenti_al_secondo),
        samplerate=numero_segmenti_al_secondo,
        channels=1,
        dtype='int16'
    )

    sounddevice.wait()
    # Salva il file WAV
    wav.write('registrazione_del_vocale.wav', numero_segmenti_al_secondo, registrazione)

    # Trascrive l'audio
    trascrittore = speech_recognition.Recognizer()

    with speech_recognition.AudioFile('registrazione_del_vocale.wav') as source:
        audio = trascrittore.record(source)
    try:
        trascrizione = trascrittore.recognize_google(audio, language='it-IT')
        return trascrizione
    except speech_recognition.UnknownValueError:
        return None  # audio non comprensibile (silenzio, rumore, ecc.)
    except speech_recognition.RequestError:
        return None  # errore di rete con il servizio Google


def traduci_con_gemini(testo: str, lingua_partenza: str, lingua_destinazione: str) -> str:
    client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

    # Rendiamo le istruzioni di sistema dinamiche basandoci sulle lingue passate
    system_prompt = (
        f"Sei un traduttore bilingue professionista ed esperto in {lingua_partenza} e {lingua_destinazione}. "
        f"Il testo inserito è in {lingua_partenza}. "
        f"Il tuo compito è tradurlo fedelmente in {lingua_destinazione}, mantenendo intatto il significato originale, "
        f"il tono e le sfumature culturali. Trova gli equivalenti idiomatici corretti invece di fare una traduzione letterale. "
        f"Restituisci ESCLUSIVAMENTE la traduzione pulita, senza introduzioni, note, spiegazioni o virgolette."
    )

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
            ),
            contents=testo,
        )
        return response.text.strip() if response.text else ""
    except Exception as e:
        raise RuntimeError("Quota API Gemini esaurita. Attendi qualche minuto e riprova.") from e
