import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
import glob
from multiprocessing import Pool
import tqdm
import argparse
import functools


def split_audio(wav_file: str, working_dir: str, seconds: int, silence_threshold: int):
    """Split audio into smaller parts.

    Args:
        wav_file (str): The path of the file to split.
        working_dir (str): The working directory.
        seconds (int): The length of a segment.

    Returns:
        list[str]: List of splitted files.
    """

    filename = os.path.splitext(os.path.basename(wav_file))[0]
    audio = AudioSegment.from_wav(wav_file)
    length = round(audio.duration_seconds, 2)

    splitted_files: list[str] = []

    if length > seconds:
        chunks: list[AudioSegment] = split_on_silence(
            audio,
            min_silence_len=300,
            silence_thresh=silence_threshold,
            keep_silence=300,
        )
        current_length = 0
        current_split = 0

        out_data = AudioSegment.empty()
        for i, chunk in enumerate(chunks):
            current_length += round(chunk.duration_seconds, 2)
            if current_length > seconds or (i == len(chunks) - 1 and len(chunks) > 1):
                out_file = os.path.join(
                    working_dir, "{}_split{}.wav".format(filename, str(current_split))
                )
                splitted_files.append(out_file)
                out_data.export(out_file, format="wav")

                current_length = 0
                current_split += 1

                out_data = AudioSegment.empty()
            else:
                if out_data:
                    out_data += chunk
                else:
                    out_data = chunk

    else:
        out_file = os.path.join(working_dir, "{}.wav".format(filename))
        splitted_files.append(out_file)
        audio.export(out_file, format="wav")

    return splitted_files


def get_small_files(files: list[str], seconds=1):
    """Delete files shorter than `seconds`

    Args:
        files (list[str]): List of file paths to check.
        seconds (int, optional): The threshold. Defaults to 1.

    Returns:
        list[str]: List of deleted files.
    """

    deleted_files: list[str] = []
    for wav_file in files:
        audio: AudioSegment = AudioSegment.from_wav(wav_file)
        length = round(audio.duration_seconds, 2)

        if length < seconds:
            os.remove(wav_file)
            deleted_files.append(wav_file)
    return deleted_files


def split_audios(input_path: str, working_dir: str, args: argparse.Namespace):
    """Splits that audio into chucks of 12 seconds segment.

    Args:
        input_path (str): The input directory for audio files.
        working_dir (str): The working directory.
        args (argparse.Namespace): The programs arguments.

    Returns:
        list[str]: list of splitted files path
    """
    wav_files = sorted(glob.glob(os.path.join(input_path, "*.wav")))
    splitted_files: list[str] = []

    with Pool(args.parallel) as pool:
        pbar = tqdm.tqdm(
            pool.imap(
                functools.partial(
                    split_audio,
                    working_dir=working_dir,
                    seconds=args.segment_length,
                    silence_threshold=args.silence_threshold,
                ),
                wav_files,
            ),
            total=len(wav_files),
        )
        pbar.set_description("Splitting files")

        for r in list(pbar):
            splitted_files = splitted_files + r

        small_files = get_small_files(splitted_files, args.discard_under_second)
        splitted_files = [file for file in splitted_files if file not in small_files]

    return splitted_files
