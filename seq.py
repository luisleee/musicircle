import mido

def get_seq(filename, tracks):
    mid = mido.MidiFile(filename)
    tempo = 576923
    tpb = mid.ticks_per_beat
    arr_notes = []
    dict_tracks = {}
    for (alias, name) in tracks:
        # match the name
        tr = None
        for track in mid.tracks:
            if track.name == name:
                tr = track
                break
        if tr == None:
            continue

        # get notes in the track
        t = 0
        arr = []
        for msg in tr:
            t += mido.tick2second(msg.time, tpb, tempo)
            if msg.type == "note_on":
                arr.append((t, msg.note, alias, msg.velocity))

        # index by pitch
        arr.sort(key=lambda x: x[1])
        indexed_arr = []
        c = -1
        last = -1
        for (t, pitch, alias, vel) in arr:
            if pitch != last:
                last = pitch
                c += 1
            indexed_arr.append((t, c, alias, vel))
        dict_tracks[alias] = c

        # add 'em to the list
        arr_notes.extend(indexed_arr)
    arr_notes.sort(key=lambda x: x[0])

    return (arr_notes, dict_tracks)
