import mido

def get_seq(filename, tracks):
    mid = mido.MidiFile(filename)
    tempo = 750000
    tpb = mid.ticks_per_beat
    arr = []
    for (name, num) in tracks:
        t = 0
        for msg in mid.tracks[num]:
            t += mido.tick2second(msg.time, tpb, tempo)
            if msg.type == "note_on":
                arr.append((t, msg.note, name))
    arr.sort(key=lambda x: x[0])

    return arr
