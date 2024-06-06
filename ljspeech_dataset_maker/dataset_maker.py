import os
import shutil


def make_metadata_entries(transcribed: list[str]) -> list[str]:
    entries: list[str] = []
    for entry in transcribed:
        filename = os.path.splitext(os.path.basename(entry))[0]


def make_dataset(transcribed: list[str], working_dir: str, output_dir: str):
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    wav_dir = os.path.join(output_dir, "wav")
    if not os.path.isdir(wav_dir):
        os.makedirs(wav_dir)

    entries: list[str] = []
    for entry in transcribed:
        basename = os.path.basename(entry)
        filename = os.path.splitext(basename)[0]
        wav_file = "{}.wav".format(filename)

        with open(entry, "r") as transcription:
            entries.append(
                "{}|{}".format(wav_file, " ".join(transcription.readlines()))
            )

        shutil.move(
            os.path.join(working_dir, wav_file), os.path.join(wav_dir, wav_file)
        )

    metadata_file = os.path.join(output_dir, "metadata.csv")
    with open(metadata_file, "w") as metadata:
        metadata.write("\n".join(entries))
