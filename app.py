import os
import asyncio
import edge_tts
from docx import Document

# Male voice
VOICE = "en-US-ChristopherNeural"
# Slower speech
RATE = "-20%"

print("Starting conversion, Please wait...")

INPUT_FOLDER = "files"
OUTPUT_FOLDER = "audio"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def read_docx(filepath):
    doc = Document(filepath)

    text = "\n".join(
        para.text
        for para in doc.paragraphs
        if para.text.strip()
    )

    return text


async def convert_file(input_file, output_file):

    text = read_docx(input_file)

    communicate = edge_tts.Communicate(
        text=text,
        voice=VOICE,
        rate=RATE,
        pitch="-5Hz"
    )

    await communicate.save(output_file)

    print(f"Created: {output_file}")


async def main():

    tasks = []

    for filename in os.listdir(INPUT_FOLDER):

        if filename.endswith(".docx"):

            input_path = os.path.join(
                INPUT_FOLDER,
                filename
            )

            output_name = (
                os.path.splitext(filename)[0]
                + ".mp3"
            )

            output_path = os.path.join(
                OUTPUT_FOLDER,
                output_name
            )

            tasks.append(
                convert_file(
                    input_path,
                    output_path
                )
            )

    await asyncio.gather(*tasks)


asyncio.run(main())