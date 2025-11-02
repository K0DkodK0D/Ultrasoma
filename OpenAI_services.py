from openai import OpenAI
client = OpenAI(api_key="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")

def generateAnswer(message):
    prompt = (
        "Ti chiami Ultrasoma, sei un robot intelligente impiegato in un contesto esclusivamente didattico e illustrativo. "
        "Ti potranno essere fatte domande generali, specifiche in base all'ambiente in cui ti trovi "
        "(per esempio un Museo, una Mostra d'Arte, un Laboratorio scolastico...), tu dovrai rispondere"
        "in maniera simpatica, solo ed esclusivamente discorsiva (NO ELENCHI), e quando necessario esplicativa."
        "Non superare i 300 caratteri per domande generali. Non terminare con una domanda."
    )

    response = client.responses.create(
        model="gpt-4o-mini",
        instructions=prompt,
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": f" {message}"},
                ]
            }
        ]
    )

    return response.output_text

print(generateAnswer("Spiega il senso della vita"))
