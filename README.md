# Simple LJSpeech Dataset Maker

This is a simple LJSpeech Dataset Maker, based on [LJSpeechTools](https://github.com/lalalune/LJSpeechTools). It splits and transcribes the inputs WAV files. Underthehood, it uses Google Speech Recognition for transcriping. Single speaker only.

## Usage

1. Install the dependencies.

    ```bash
    pip install -r requirements.txt
    ```

2. Place your WAV files into the `input` folder. Mono 22khz WAV is ideal.

3. Run the pipeline.
    ```
    usage: pipeline.py [-h] [-p PARALLEL] [-l SEGMENT_LENGTH] [-s SILENCE_THRESHOLD] [-d DELAY]

    LJSpeech Dataset Maker

    options:
    -h, --help            show this help message and exit
    -p PARALLEL, --parallel PARALLEL
                            Number of running process. Default is your core/thread count minus 2.
    -l SEGMENT_LENGTH, --segment-length SEGMENT_LENGTH
                            The length of a sengment, in seconds. Default is 12 seconds.
    -s SILENCE_THRESHOLD, --silence-threshold SILENCE_THRESHOLD
                            The silence threshold for splitting, in dBFS (negative integer). Default is -40.
    -d DELAY, --delay DELAY
                            Add a delay to online transcription, in senconds. Default is 0.1 second.
    -u DISCARD_UNDER_SECOND, --discard-under-second DISCARD_UNDER_SECOND
                            Discard any segment under this length, in senconds. Default is 1 second.
    ```

4. The output dataset will be in the `dataset` folder.