import os.path as path
import os

label_to_int = {
    "large-vehicle": 0,
    "swimming-pool": 1,
    "helicopter": 2,
    "bridge": 3,
    "plane": 4,
    "ship": 5,
    "soccer-ball-field": 6,
    "basketball-court": 7,
    "ground-track-field": 8,
    "small-vehicle": 9,
    "harbor": 10,
    "baseball-diamond": 11,
    "tennis-court": 12,
    "roundabout": 13,
    "storage-tank": 14,
    "container-crane": 15,
}

def convert(data_folder):
    labels_folder = os.path.join(data_folder, "dota_labels")
    if not (os.path.exists(labels_folder) and os.path.isdir(labels_folder)):
        return
    for fname in os.listdir(labels_folder):
        if fname.startswith('.'):
            # ignore dot files
            continue
        new_labels_folder = labels_folder.replace('dota_', '')
        with open(path.join(labels_folder, fname), 'r') as f:
            source = f.readline()
            gsd = f.readline()
            with open(path.join(new_labels_folder, fname), 'w') as nf:
                for label in f:
                    things = label.split(' ')
                    x1, y1, x2, y2, x3, y3, x4, y4 = map(float, things[:8])
                    category = label_to_int[things[8]]
                    # category = things[8]
                    difficult = things[9]  # not used now
                    xmin = min(x1, x2, x3, x4)
                    xmax = max(x1, x2, x3, x4)
                    ymin = min(y1, y2, y3, y4)
                    ymax = max(y1, y2, y3, y4)
                    print(f'{category} {(xmax-xmin)/2+xmin} {(ymax-ymin)/2+ymin} {xmax-xmin} {ymax-ymin}', file=nf)
                    # print(f'{category} {xmin} {ymin} {xmax} {ymax}', file=nf)

if __name__ == '__main__':
    convert('data/dota')