import mido
from mido import MidiFile, MidiTrack, Message
import logging
logger = logging.getLogger(__name__)

def convert_txt_to_midi(input_file, output_file, bpm):
  """Converts a text file with timestamps and notes to a percussion MIDI file.

  Args:
      input_file: Path to the text file containing note data.
      output_file: Path to save the converted MIDI file.
      bpm: Tempo (beats per minute) for the MIDI file.
  """

  ticks_per_beat = 480  # Standard MIDI ticks per beat
  # ticks_per_second = ticks_per_beat * (bpm / 60)
  ticks_per_second = int(ticks_per_beat * (bpm / 60))
  # Create a new MIDI file with a single track
  midi_file = mido.MidiFile()
  track = mido.MidiTrack()
  midi_file.tracks.append(track)

  # Set tempo based on BPM
  tempo = mido.bpm2tempo(bpm)

  tempo_message = mido.MetaMessage('set_tempo', tempo=tempo)
  track.append(tempo_message)

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
    # ticks = mido.second2tick(time, midi_file.ticks_per_beat, tempo)
    ticks = int(time * ticks_per_second)
    # ticks = int(time * (ticks_per_beat * bpm / 60))
    # Add a note_on event
    track.append(mido.Message('note_on', note=note, velocity=100, time=ticks, channel=9))

        # Add a note_off event (you may want to adjust the duration)
    track.append(mido.Message('note_off', note=note, velocity=0, time=ticks + 1, channel=9))

  # Save the converted MIDI file
  midi_file.save(output_file)

# Example usage
input_file = "waitforyou_plave.txt"  # Replace with your text file path
output_file = "waitforyou_plave.mid"
bpm = 95  # Set your desired BPM

convert_txt_to_midi(input_file, output_file, bpm)
print(f"Converted MIDI file saved to: {output_file}")

logger.info("Converted MIDI file saved to: %s", output_file)
