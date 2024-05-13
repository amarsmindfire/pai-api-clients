import io
import os
import shutil

from django.conf import settings

import librosa
import soundfile
from google.cloud import speech_v1p1beta1 as speech
from pydub import AudioSegment

from .constants import DEFAULT_CHUNK_SIZE


def normalize_transcript(response, count=0):
    combined_transcript = ""
    alternatives = []

    for result in response.results:
        for alternative in result.alternatives:
            if not alternative.words:
                continue

            combined_transcript += alternative.transcript + "<br>"
            alternatives.append({
                'transcript': alternative.transcript,
                'confidence': alternative.confidence,
                'start_time': alternative.words[0].start_time.total_seconds() + (count * DEFAULT_CHUNK_SIZE),
                'end_time': alternative.words[-1].end_time.total_seconds() + (count * DEFAULT_CHUNK_SIZE)
            })

    return combined_transcript.strip(), alternatives


def audio_sampling(file, sampling_rate=8000):
    audio_array, sr = librosa.load(file, sr=sampling_rate)

    filepath = os.path.split(file)
    filepath, filename = filepath[0], filepath[1]
    filename = f"{''.join(filename.split('.')[:-1])}.wav"

    file = os.path.join(filepath, filename)
    soundfile.write(file, audio_array, sr, format='WAV', subtype='PCM_24')

    return file


class Extractor:
    def __init__(self, filepath, diarization):
        self.tmp_dir = os.path.join(settings.MEDIA_ROOT, 'tmp')
        if not os.path.isdir(self.tmp_dir):
            os.mkdir(self.tmp_dir)

        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = settings.GOOGLE_APPLICATION_CREDENTIALS
        self.config = None
        self.audio = None
        self.base_filepath = filepath
        self.diarization = diarization
        self.client = speech.SpeechClient()
        self.chunk_files = []
        self.transcript = ""
        self.alternatives = []
        self.make_chunks()
        self.process_audio_file(filepath)
        self.create_defaults()
        self.responses = []
        self.start_time = None
        self.end_time = None

    def process_audio_file(self, file):
        if not os.path.isfile(file):
            raise Exception("File doesn't exists")

        with io.open(file, "rb") as audio_file:
            content = audio_file.read()

        file_format = file.split('.')[-1]

        recording = AudioSegment.from_file(io.BytesIO(content), format=file_format)
        recording.export(file, format='mp3')

        with io.open(file, "rb") as audio_file:
            content = audio_file.read()

        self.audio = speech.RecognitionAudio(content=content)

    def create_defaults(self):
        try:
            self.config = speech.RecognitionConfig(
                sample_rate_hertz=44100,
                enable_automatic_punctuation=True,
                language_code="en-US",
                enable_word_time_offsets=True,
                model='phone_call',
                use_enhanced=True,
                enable_speaker_diarization=self.diarization,
                diarization_speaker_count=2,
                enable_word_confidence=True,
            )
        except Exception as e:
            print(e)

    def run(self):
        self.transcript = ""
        for count, file in enumerate(self.chunk_files):
            file = audio_sampling(file)
            self.process_audio_file(file)
            try:
                response = self.client.recognize(config=self.config, audio=self.audio)

                if response:
                    self.responses.append(response)
                    combined_transcript, alternatives = normalize_transcript(response, count)
                    self.transcript += combined_transcript + " "
                    if not self.diarization:
                        self.alternatives += alternatives
            except Exception as e:
                raise Exception(e)

        if self.diarization:
            self.alternatives = self.normalize_transcript()
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

        return {"data": self.transcript.strip(), "alternatives": self.alternatives}

    def make_chunks(self):
        sound = AudioSegment.from_mp3(self.base_filepath)
        duration_in_milliseconds = len(sound)

        if duration_in_milliseconds < 60000:
            self.chunk_files.append(self.base_filepath)
            return

        # split sound1 in 55-second slices
        audio_chunks = sound[::DEFAULT_CHUNK_SIZE * 1000]

        for i, chunk in enumerate(audio_chunks):
            out_file = f"{self.tmp_dir}/chunk_{i}.mp3"
            self.chunk_files.append(out_file)
            chunk.export(out_file, format="mp3")

    def normalize_transcript(self):
        res = []
        for count, response in enumerate(self.responses):

            curr_speaker = None
            word_str = ''
            confidence = []
            last_result = response.results[-1]
            self.start_time = None

            for alternative in last_result.alternatives:
                if not alternative.words:
                    continue

                for word in alternative.words:
                    if self.start_time is None:
                        self.start_time = word.start_time.total_seconds()

                    if curr_speaker is None:
                        curr_speaker = word.speaker_tag

                    elif curr_speaker != word.speaker_tag:
                        res.append({
                            'speaker': curr_speaker,
                            'transcript': word_str,
                            'start_time': max(self.start_time + (count * DEFAULT_CHUNK_SIZE), 0.0),
                            'end_time': self.end_time + (count * DEFAULT_CHUNK_SIZE),
                            'confidence': round(sum(confidence) / len(confidence), 4)
                        })
                        curr_speaker = word.speaker_tag
                        self.start_time = self.end_time
                        word_str = ''
                        confidence = []

                    word_str += word.word + " "
                    confidence.append(word.confidence)
                    self.end_time = word.end_time.total_seconds()

                res.append({
                    'speaker': curr_speaker,
                    'transcript': word_str,
                    'start_time': max(self.start_time + (count * DEFAULT_CHUNK_SIZE), 0.0),
                    'end_time': self.end_time + (count * DEFAULT_CHUNK_SIZE),
                    'confidence': round(sum(confidence) / len(confidence), 4)
                })
        return res
