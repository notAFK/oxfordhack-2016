import argparse
import glob
import midi_helpers
import numpy as np
import os
import rbm
import tensorflow as tf

parser = argparse.ArgumentParser(description='Train a neural network to generate songs.')

parser.add_argument('input_dir',
                    help='directory from where songs (acting as training data) will be loaded')

parser.add_argument('--output_dir',
                    metavar='PATH',
                    help='directory where generated songs will be saved',
                    default='output')

parser.add_argument('--sample_length',
                    metavar='N',
                    help='length of generated song',
                    type=int,
                    default=65)

parser.add_argument('--num_samples',
                    metavar='N',
                    help='number of samples to generate',
                    type=int,
                    default=1)

parser.add_argument('--num_epochs',
                    metavar='N',
                    help='number of epochs to train for',
                    type=int,
                    default=4000)

args = parser.parse_args()

def _preprocess_songs(songs, sample_length):
    # Songs are stored in time * notes format. Song length = song_timesteps * 2 * note_range.
    # We reshape songs so that each input is a vector of size sample_length * 2 * note_range.
    preprocessed_songs = []

    for song in songs:
        song = np.array(song)
        num_samples = int(song.shape[0] / sample_length)
        song = song[:num_samples * sample_length]
        samples = np.reshape(song, [num_samples, song.shape[1] * sample_length])
        preprocessed_songs.extend(samples)

        # If taking 60 samples at a time and the song has 200 samples, 60 * 3 = 180 so the last 20
        # samples are ignored. We add the last 60 samples to maximize data efficiency.
        last_sample = np.reshape(song[-sample_length:], [song.shape[1] * sample_length])
        preprocessed_songs.append(last_sample)

    return np.array(preprocessed_songs)


def _get_songs(path, min_length):
    songs = []
    for f in glob.glob('{}/*.mid*'.format(path)):
        song = np.array(midi_helpers.midi_to_note_state_matrix(f))
        if np.array(song).shape[0] > 50:
            songs.append(song)
    return songs
 

songs = _get_songs(args.input_dir, min_length=args.sample_length)
samples = _preprocess_songs(songs, args.sample_length)

print('Loaded {} songs. Created {} samples.'.format(len(songs), len(samples)))

num_visible = 2 * args.sample_length * midi_helpers.note_range
network = rbm.RBM(num_visible,
                  num_hidden=50,
                  learning_rate=0.01,
                  batch_size=32,
                  num_epochs=args.num_epochs)

print('Training...')
network.fit(samples)

print('Generating...')
samples = network.generate(np.zeros([1, num_visible]))
samples = np.round(samples)

if not os.path.isdir(args.output_dir):
	os.mkdir(args.output_dir)

for i in range(samples.shape[0]):
    # Reshape vector to time * notes and save as a MIDI file.
    state_matrix = np.reshape(samples[i, :], [args.sample_length, 2 * midi_helpers.note_range])
    output_path = os.path.join(args.output_dir, 'song_{}'.format(i))
    midi_helpers.note_state_matrix_to_midi(state_matrix, output_path)