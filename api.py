import google.generativeai as genai
genai.configure(api_key="AIzaSyCzsws5s0uqzvtVV5aEUsvaAosixm-AGnI")
model = genai.GenerativeModel('gemini-2.5-flash')
response = model.generate_content("Generami un codice python che trascriva un testo vocale in italiano e lo traduca in siciliano senza commenti e spiegazioni")
print(response.text)