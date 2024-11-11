import os
import tempfile
import wave
import pyaudio
import keyboard
import pyautogui
import pyperclip
from groq import Groq

client = Groq(api_key="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")


def grabar_audio(frecuencia_mestreo=16000, canales=1, fragmento=1024):
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=canales,
        rate=frecuencia_mestreo,
        input=True,
        frames_per_buffer=fragmento,
    )
    print("Presiona y manten presionado el Boton INS para comenzar a grabar...")
    frames = []
    keyboard.wait("insert")
    print("Grabando... (Suelta INS para detener)")

    try:
        while keyboard.is_pressed("insert"):
            try:
                data = stream.read(fragmento, exception_on_overflow=False)
                frames.append(data)
            except IOError as e:
                print(f"Error al leer el audio: {e}")
                break
    finally:
        print("Grabacion finalizada.")
        stream.stop_stream()
        stream.close()
        p.terminate()

    return frames, frecuencia_mestreo


def guardar_audio(frames, frecuencia_muestreo):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as audio_temp:
        wf = wave.open(audio_temp.name, "wb")
        wf.setnchannels(1)
        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
        wf.setframerate(frecuencia_muestreo)
        wf.writeframes(b"".join(frames))
        wf.close()
        return audio_temp.name


def transcribir_audio(ruta_archivo_audio):
    try:
        with open(ruta_archivo_audio, "rb") as archivo:
            transcripcion = client.audio.transcriptions.create(
                file=(os.path.basename(ruta_archivo_audio), archivo.read()),
                model="whisper-large-v3",
                prompt="""El audio es de una persona normal trabajando y su necesidad es transcribir el audio""",  # el audio es de una persona normal trabajando
                response_format="text",
                language="es",
            )
        return transcripcion
    except Exception as e:
        print(f"Ocurrio un error: {str(e)}")
        return None


def copiar_transcripcion_al_porta_papeles(texto):
    pyperclip.copy(texto)
    pyautogui.hotkey("ctrl", "v")


def main():
    while True:
        frames, frecuencia_muestreo = grabar_audio()
        archivo_audio_temp = guardar_audio(frames, frecuencia_muestreo)
        print("Transcribiendo...")
        transcripcion = transcribir_audio(archivo_audio_temp)

        if transcripcion:
            print("\nTranscripcion:")
            print("COpiando transcripcion al portapapeles...")
            copiar_transcripcion_al_porta_papeles(transcripcion)
            print("Transcripcion copiada al portapapeles y pegada en la aplicacion.")
        else:
            print("La transcripcion fallo.")

        os.unlink(archivo_audio_temp)
        print("\nListo para la proxima grabacion. Presiona INS para comenzar.")


if __name__ == "__main__":
    main()
