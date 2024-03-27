import mido
from mido import MidiFile, MidiTrack, Message, MetaMessage
import logging

logger = logging.getLogger(__name__)

def convert_txt_to_midi(input_file, output_file, bpm):
  """Converts a text file with timestamps and notes to a percussion MIDI file.

  Args:
      input_file: Path to the text file containing note data.
      output_file: Path to save the converted MIDI file.
      bpm: Tempo (beats per minute) for the MIDI file.
  """

  
  # ticks_per_second = int(ticks_per_beat * bpm / 60)
  # Create a new MIDI file with a single track
  midi_file = mido.MidiFile()
  track = mido.MidiTrack()
  midi_file.tracks.append(track)

  

  # ticks_per_beat = 480  # Standard MIDI ticks per beat
  ticks_per_beat = midi_file.ticks_per_beat
 
  # ticks_per_second = ticks_per_beat * (bpm / 60)
  ticks_per_second = ticks_per_beat * bpm / 60
  # ticks_per_second = ticks_per_beat * 1000000.0 / bpm
  # Set tempo based on BPM
  # tempo = mido.bpm2tempo(bpm)
  tempo_message = mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(bpm))
  track.append(tempo_message)
  last_tick = 0

  # Read data from the text file
  with open(input_file, 'r') as f:
    lines = f.readlines()

  # Process each line, converting to MIDI messages
  for line in lines:
    # Split line by tab delimiter
    time, note = line.strip().split('\t')

    # Print the values of time and note
    print(f"Time: {time}, Note: {note}")

    # Convert time string to seconds (assuming seconds format)
    time = float(time)

    # Convert note string to integer (MIDI note number)
    note = int(note)

    # Convert the time in seconds to ticks
    # ticks = mido.second2tick(time, midi_file.ticks_per_beat, tempo)
    ticks = int(time * ticks_per_second)
    #Added
    current_tick = int(round(time * ticks_per_second))
    delta = current_tick - last_tick
    # ticks = int(time * (ticks_per_beat * bpm / 60))
    # Add a note_on event
    track.append(mido.Message('note_on', note=note, velocity=64, time=delta, channel=9))

        # Add a note_off event (you may want to adjust the duration)
    track.append(mido.Message('note_off', note=note, velocity=64, time=int(round(0.1*ticks_per_second)), channel=9))
    last_tick = current_tick
  print(f"ticks_per_beat: {ticks_per_beat}")
  # Get the length of the MIDI file in seconds
  song_length = midi_file.length
  # Print the song length
  print(f"Song length: {song_length} seconds")

  # Save the converted MIDI file
  midi_file.save(output_file)

# Example usage
input_file = "waitforyou_plave.txt"  # Replace with your text file path
output_file = "waitforyou_plave.mid"
bpm = 127  # Set your desired BPM

convert_txt_to_midi(input_file, output_file, bpm)
print(f"Converted MIDI file saved to: {output_file}")

logger.info("Converted MIDI file saved to: %s", output_file)
