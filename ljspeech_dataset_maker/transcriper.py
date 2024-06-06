from multiprocessing import Pool
import tqdm
import functools
import argparse
import speech_recognition as sr
import os
import time


CENSORED_WORDS = {
    "f******": "ucking",
    "f*****": "ucks",
    "f*****": "ucked",
    "f***": "uck",
    "s***": "hit",
    "s*******": "hitting",
    "s***": "hitty",
    "s****": "hits",
    "n*****": "iggas",
    "n****": "igga",
    "b****": "itch",
}


def transcribe_file(
    wav_file: str, working_dir: str, recognizer: sr.Recognizer, args: argparse.Namespace
) -> str | None:
    with sr.AudioFile(wav_file) as source:
        audio = recognizer.record(source)
        transcription = ""
        filename = os.path.splitext(os.path.basename(wav_file))[0]
        filepath = os.path.join(working_dir, "{}.txt".format(filename))

        try:
            transcription: str = recognizer.recognize_google(audio)
            time.sleep(args.delay)

            # Fix censored words
            for censored_word in CENSORED_WORDS:
                uncensored_word = censored_word[0] + CENSORED_WORDS[censored_word]
                transcription.replace(censored_word, uncensored_word)

            with open(filepath, "w") as out:
                out.write(transcription)

            return filepath
        except:
            return None


def transcripe(
    wav_files: list[str], working_dir: str, args: argparse.Namespace
) -> list[str]:
    """Transcripe and return list of files"""
    recognizer = sr.Recognizer()

    with Pool(args.parallel) as pool:
        pbar = tqdm.tqdm(
            pool.imap(
                functools.partial(
                    transcribe_file,
                    working_dir=working_dir,
                    recognizer=recognizer,
                    args=args,
                ),
                wav_files,
            ),
            total=len(wav_files),
        )
        pbar.set_description("Transcripting files")

        transcribed = [r for r in list(pbar) if r is not None]

        return transcribed
