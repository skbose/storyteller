import os
import re
import tempfile
import torch
from torch.nn import functional as F
import numpy as np
import commons
from vits import utils as myutils
import argparse
import subprocess
from data_utils import TextAudioLoader, TextAudioCollate, TextAudioSpeakerLoader, TextAudioSpeakerCollate
from models import SynthesizerTrn
from typing import List
import re

from scipy.io.wavfile import write
import scipy


import os
import subprocess
import locale
locale.getpreferredencoding = lambda: "UTF-8"


def preprocess_char(text, lang=None):
    """
    Special treatement of characters in certain languages
    """
    print(lang)
    if lang == 'ron':
        text = text.replace("ț", "ţ")
    return text


class TextMapper(object):
    def __init__(self, vocab_file):
        self.symbols = [x.replace("\n", "") for x in open(vocab_file, encoding="utf-8").readlines()]
        self.SPACE_ID = self.symbols.index(" ")
        self._symbol_to_id = {s: i for i, s in enumerate(self.symbols)}
        self._id_to_symbol = {i: s for i, s in enumerate(self.symbols)}

    def text_to_sequence(self, text, cleaner_names):
        '''Converts a string of text to a sequence of IDs corresponding to the symbols in the text.
        Args:
        text: string to convert to a sequence
        cleaner_names: names of the cleaner functions to run the text through
        Returns:
        List of integers corresponding to the symbols in the text
        '''
        sequence = []
        clean_text = text.strip()
        for symbol in clean_text:
            symbol_id = self._symbol_to_id[symbol]
            sequence += [symbol_id]
        return sequence

    def uromanize(self, text, uroman_pl):
        iso = "xxx"
        with tempfile.NamedTemporaryFile() as tf, \
             tempfile.NamedTemporaryFile() as tf2:
            with open(tf.name, "w") as f:
                f.write("\n".join([text]))
            cmd = f"perl " + uroman_pl
            cmd += f" -l {iso} "
            cmd +=  f" < {tf.name} > {tf2.name}"
            os.system(cmd)
            outtexts = []
            with open(tf2.name) as f:
                for line in f:
                    line =  re.sub(r"\s+", " ", line).strip()
                    outtexts.append(line)
            outtext = outtexts[0]
        return outtext

    def get_text(self, text, hps):
        text_norm = self.text_to_sequence(text, hps.data.text_cleaners)
        if hps.data.add_blank:
            text_norm = commons.intersperse(text_norm, 0)
        text_norm = torch.LongTensor(text_norm)
        return text_norm

    def filter_oov(self, text):
        val_chars = self._symbol_to_id
        txt_filt = "".join(list(filter(lambda x: x in val_chars, text)))
        print(f"text after filtering OOV: {txt_filt}")
        return txt_filt


def preprocess_text(txt, text_mapper, hps, uroman_dir=None, lang=None):
    txt = preprocess_char(txt, lang=lang)
    is_uroman = hps.data.training_files.split('.')[-1] == 'uroman'
    if is_uroman:
        with tempfile.TemporaryDirectory() as tmp_dir:
            if uroman_dir is None:
                cmd = f"git clone git@github.com:isi-nlp/uroman.git {tmp_dir}"
                print(cmd)
                subprocess.check_output(cmd, shell=True)
                uroman_dir = tmp_dir
            uroman_pl = os.path.join(uroman_dir, "bin", "uroman.pl")
            print(f"uromanize")
            txt = text_mapper.uromanize(txt, uroman_pl)
            print(f"uroman text: {txt}")
    txt = txt.lower()
    txt = text_mapper.filter_oov(txt)
    return txt


def download(lang, tgt_dir="./"):
  lang_fn, lang_dir = os.path.join(tgt_dir, lang+'.tar.gz'), os.path.join(tgt_dir, lang)
  if os.path.exists(lang_dir):
      print ("Model already downloaded")
      return lang_dir

  cmd = ";".join([
        f"wget https://dl.fbaipublicfiles.com/mms/tts/{lang}.tar.gz -O {lang_fn}",
        f"tar zxvf {lang_fn}"
  ])
  print(f"Download model for language: {lang}")
  subprocess.check_output(cmd, shell=True)
  print(f"Model checkpoints in {lang_dir}: {os.listdir(lang_dir)}")
  return lang_dir


class TTS:
    def __init__(self) -> None:
        '''
        Initialize the TTS model
        '''
        if torch.cuda.is_available():
            self.device = torch.device("cuda")
        else:
            self.device = torch.device("cpu")

        self.LANG = "eng"
        self.ckpt_dir = download(self.LANG)

        print(f"Run inference with {self.device}")
        vocab_file = f"{self.ckpt_dir}/vocab.txt"
        config_file = f"{self.ckpt_dir}/config.json"
        assert os.path.isfile(config_file), f"{config_file} doesn't exist"
        self.hps = myutils.get_hparams_from_file(config_file)
        self.text_mapper = TextMapper(vocab_file)
        self.net_g = SynthesizerTrn(
            len(self.text_mapper.symbols),
            self.hps.data.filter_length // 2 + 1,
            self.hps.train.segment_size // self.hps.data.hop_length,
            **self.hps.model)
        self.net_g.to(self.device)
        _ = self.net_g.eval()

        g_pth = f"{self.ckpt_dir}/G_100000.pth"
        print(f"load {g_pth}")

        _ = myutils.load_checkpoint(g_pth, self.net_g, None)
    
    def split_paragraph_into_sentences(self, paragraph: str):
        COMMA = "[COMMA]"
        FULLSTOP = "[FULLSTOP]"
        EXCLAMATION = "[EXCLAMATION]"
        '''
        Split paragraph into sentences
        @param paragraph: paragraph to split
        @return: list of sentences
        '''
        paragraph = paragraph.replace(".", f" {FULLSTOP}")
        paragraph = paragraph.replace(",", f" {COMMA}")
        paragraph = paragraph.replace("!", f" {EXCLAMATION}")
        
        words = paragraph.split()
        print (words)
        sentences = []
        sentence = []
        for word in words:
            if COMMA in word or FULLSTOP in word or EXCLAMATION in word:
                if word == COMMA:
                    pause = 0.5
                if word == FULLSTOP:
                    pause = 1
                if word == EXCLAMATION:
                    pause = 2

                sentences.append((" ".join(sentence), pause))
                sentence = []
            # if word is not a punctuation mark add to sentence
            else:
                sentence.append(word)
                
        return sentences

    def generate_speech_for_paragraph(self, paragraph: str):
        # split paragraph into sentences
        sentences_with_pauses = self.split_paragraph_into_sentences(paragraph)
        # generate speech for each sentence
        audios = []
        for each in sentences_with_pauses:
            sentence = each[0]
            pause = each[1]
            print(f"sentence: {sentence}")
            sentence_audio = self.generate_speech_for_sentence(sentence)
            audios.append((sentence_audio, pause))
        
        audio = self.merge_wav_audios(audios)
        return audio
    
    def merge_wav_audios(self, audios: List[tuple]):
        '''
        Merge wav audios with pauses
        @param audios: list of audio arrays with pauses
        @return: merged audio array
        '''
        # pad audios with pauses
        audios = [np.pad(audio, (0, int(pause * 1000))) for (audio,pause) in audios]
        # merge audios
        audio = np.concatenate(audios)
        return audio

    def generate_speech_for_sentence(self, txt: str):
        '''Generate speech from text
        @param txt: input text
        @return: speech audio
        '''
        txt = preprocess_text(txt, self.text_mapper, self.hps, lang=self.LANG)
        stn_tst = self.text_mapper.get_text(txt, self.hps)
        with torch.no_grad():
            x_tst = stn_tst.unsqueeze(0).to(self.device)
            x_tst_lengths = torch.LongTensor([stn_tst.size(0)]).to(self.device)
            hyp = self.net_g.infer(
                x_tst, x_tst_lengths, noise_scale=.667,
                noise_scale_w=0.8, length_scale=1.0
            )[0][0,0].cpu().float().numpy()
            return hyp

    def save(self, audio: np.ndarray, filename: str):
        sampling_rate = self.hps.data.sampling_rate
        scipy.io.wavfile.write(filename, rate=sampling_rate, data=audio)
        print(f"Saved to {filename}")


if __name__ == "__main__":
    paragraph = '''
    The sun was shining brightly on the green meadow where the race was to take place. The rabbit, with its fluffy tail and fast little legs, was feeling particularly confident. "I will surely win this race," it said to itself. "No one can beat me!" 
    Just then, a slow and steady tortoise came hopping along the path. "I will win this race," it said to itself. "I am much slower than you, but I will not stop until I reach the finish line."
    The race began, and the rabbit took off like a shot. It zipped and zapped along the meadow, its little legs moving as fast as they could. But the tortoise didn't give up. It plodded along slowly but surely, never stopping or resting.
    The rabbit was getting tired, but it didn't want to give up. It pushed itself harder and harder, but no matter how fast it ran, the tortoise was always right behind it.
    In the end, the tortoise crossed the finish line first! The rabbit was amazed and a bit sad. "I should have taken it easier," it said to itself.
    From that day on, the rabbit learned a valuable lesson: you should never underestimate someone just because they are slow and steady. Because sometimes, slow and steady can win the race!
    '''
    tts = TTS()
    audio_sample = tts.generate_speech_for_paragraph(paragraph=paragraph)
    tts.save(audio_sample, "hello_world.wav")
