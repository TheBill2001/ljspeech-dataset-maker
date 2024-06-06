import os
import glob
import shutil
import argparse
import multiprocessing
import tempfile

from ljspeech_dataset_maker import audiospliter, transcriper, dataset_maker


INPUT_DIR = "./input"
OUTPUT_DIR = "./dataset"


def main(args: argparse.Namespace):
    with tempfile.TemporaryDirectory() as working_dir:
        print('Working directory: "{}"'.format(working_dir))

        print("\nStarting splitting files...")
        splitted_files = audiospliter.split_audios(INPUT_DIR, working_dir, args=args)
        print(
            "Finished splitting input into {} segment(s).".format(len(splitted_files))
        )

        print("\nStarting transcriping {} segment(s)...".format(len(splitted_files)))
        transcriped = transcriper.transcripe(splitted_files, working_dir, args)
        print("Succesfully transcriped {} segment(s).".format(len(transcriped)))

        print("\nMaking the dataset, only transcriped segments will be exported...")
        dataset_maker.make_dataset(transcriped, working_dir, OUTPUT_DIR)

        print("\nDone!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LJSpeech Dataset Maker")
    parser.add_argument(
        "-p",
        "--parallel",
        help="Number of running process. Default is your core/thread count minus 2.",
        default=multiprocessing.cpu_count() - 2,
    )
    parser.add_argument(
        "-l",
        "--segment-length",
        help="The length of a sengment, in seconds. Default is 12 seconds.",
        type=int,
        default=12,
    )
    parser.add_argument(
        "-s",
        "--silence-threshold",
        help="The silence threshold for splitting, in dBFS (negative integer). Default is -40.",
        type=int,
        default=-40,
    )
    parser.add_argument(
        "-d",
        "--delay",
        help="Add a delay to online transcription, in senconds. Default is 0.1 second.",
        type=float,
        default=0.1,
    )
    parser.add_argument(
        "-u",
        "--discard-under-second",
        help="Discard any segment under this length, in senconds. Default is 1 second.",
        type=float,
        default=1,
    )

    main(parser.parse_args())
