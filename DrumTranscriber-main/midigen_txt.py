import mido
from mido import MidiFile, MidiTrack, Message, MetaMessage
import logging

logger = logging.getLogger(__name__)

def convert_txt_to_midi(input_file, output_file, bpm):
    # Create a new MIDI file with a single track
    midi_file = MidiFile()
    track = MidiTrack()
    midi_file.tracks.append(track)

    # Set tempo based on BPM
    ticks_per_beat = midi_file.ticks_per_beat
    ticks_per_second = ticks_per_beat * bpm / 60

    tempo_message = MetaMessage('set_tempo', tempo=mido.bpm2tempo(bpm))
    track.append(tempo_message)

    last_tick = 0
    max_tick = 0  # Track the maximum tick value

    # Read data from the text file
    with open(input_file, 'r') as f:
        lines = f.readlines()

    # Process each line, converting to MIDI messages
    for line in lines:
        # Split line by tab delimiter
        time, note = line.strip().split('\t')

        # Convert time string to seconds (assuming seconds format)
        time = float(time)

        # Convert note string to integer (MIDI note number)
        note = int(note)

        # Convert the time in seconds to ticks
        current_tick = int(round(time * ticks_per_second))
        delta = current_tick - last_tick

        # Update max_tick
        max_tick = max(max_tick, current_tick)

        # Add a note_on event
        track.append(Message('note_on', note=note, velocity=64, time=delta, channel=9))

        # Add a note_off event (you may want to adjust the duration)
        track.append(Message('note_off', note=note, velocity=64, time=int(round(0.1*ticks_per_second)), channel=9))

        last_tick = current_tick

    # Set the end of the track based on the maximum tick value
    track.append(MetaMessage('end_of_track', time=max_tick))

    # Get the length of the MIDI file in seconds
    song_length = max_tick / ticks_per_second

    # Print the song length
    print(f"Song length: {song_length} seconds")

    # Save the converted MIDI file
    midi_file.save(output_file)

# Example usage
input_file = "Way4Luved3.txt"  # Replace with your text file path
output_file = "Way4Luved3.mid"
bpm = 127  # Set your desired BPM

convert_txt_to_midi(input_file, output_file, bpm)
print(f"Converted MIDI file saved to: {output_file}")

logger.info("Converted MIDI file saved to: %s", output_file)
