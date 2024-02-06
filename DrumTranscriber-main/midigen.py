import mido
from mido import MidiFile, MidiTrack, Message, MetaMessage

#original 
def create_midi(times, filename, tempo):
    midi = mido.MidiFile()
    track = mido.MidiTrack()
    midi.tracks.append(track)

    track.append(mido.MetaMessage('set_tempo', tempo=tempo))

    ticks_per_beat = midi.ticks_per_beat
    ticks_per_second = ticks_per_beat * 1000000.0 / tempo
    note = 42

    last_tick = 0
    for time in times:
        current_tick = int(round(time * ticks_per_second))
        delta = current_tick - last_tick
        track.append(mido.Message('note_on', note=note, velocity=64, time=delta))
        track.append(mido.Message('note_off', note=note, velocity=64, time=int(round(0.1*ticks_per_second))))
        last_tick = current_tick

    midi.save(filename)

#Renewal code 
def create_drum_midi(csv_file, midi_file, bpm):

    ticks_per_beat = mido.MidiFile().ticks_per_beat
    ticks_per_second = ticks_per_beat * (bpm / 60)

    midi = MidiFile()
    track = MidiTrack()
    midi.tracks.append(track)

    # Add a tempo change message to set the desired BPM
    tempo = int(60000000 / bpm)
    track.append(MetaMessage('set_tempo', tempo=tempo))

    # track.append(mido.MetaMessage('set_tempo', tempo=tempo))

    with open(csv_file, 'r') as file:
        # Skip the header
        next(file)

        for line in file:
            # data = line.strip().split('\t')
            data = line.strip().split(',')
            time_seconds = float(data[6])
            # time = data[6]
            drum_type = data[7]
            # Convert confidence percentage to float
            confidence = float(data[8].strip('%')) / 100.0
            # try:
            #     time = float(data[6])
            #     drum_type = data[7]
            #     confidence = float(data[8].strip('%')) / 100.0
            # except (IndexError, ValueError):
            #     # Skip this line if there's an issue with the data
            #     continue

            # Set up the drum note mapping (adjust as needed)
            drum_mapping = {
                'crash': 49,
                'hihat_c': 42,
                'kick_drum': 36,
                'ride': 51,
                'snare': 38,
                'tom_h': 50
                # Add more mappings if needed
            }

            # Check if the drum type is in the mapping
            if drum_type in drum_mapping:
                note = drum_mapping[drum_type]

                # Adjust velocity based on confidence level
                velocity = int(confidence * 127)

                # Calculate time in ticks based on BPM
                time_ticks = int(time_seconds * ticks_per_second)

                # Add note-on and note-off messages to the MIDI track
                track.append(Message('note_on', note=note, velocity=velocity, time=time_ticks))
                track.append(Message('note_off', note=note, velocity=0, time=0))

    # Save the MIDI file
    midi.save(midi_file)

