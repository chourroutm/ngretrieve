# ngvolbox ⏹️
Script to replace volumes by their bounding box in a Neuroglancer link or state

## Dependencies

- cloud-volume[zarr]
- neuroglancer
- numpy

Install all of them with:

```bash
pip install cloud-volume[zarr] neuroglancer numpy
```

## Usage

Pass either a Neuroglancer URL (`--url`) between single quotes or the path to a JSON file with a Neuroglancer state (`--json`).

```bash
python volume_to_bbox.py --url 'https://neuroglancer-demo.appspot.com/#!...' [--process-only "layer1" "layer2"...] [--ignore-non-visible] [--keep-volume] [--suffix "_bbox"]
```

```bash
python volume_to_bbox.py --json '/path/to/state.json' [--process-only "layer1" "layer2"...] [--ignore-non-visible] [--keep-volume] [--suffix "_bbox"]
```

By default, volume layers (i.e. images and segmentations) are replaced by their bounding box (as a new annotation layer).

With the boolean argument `--keep-volume` ¦ `-k`, the volume layer is not replaced and the new annotation layer is created with "_bbox" (or any string passed with `--suffix` ¦ `-s`) appended to the layer name.

With the argument `--ignore-non-visible` ¦ `-i`, layers that are not visible (layer name is ~~strikethrough~~) are not processed.

With the argument `--process-only` ¦ `-l`, only the listed layer(s) is/are processed (takes precedence over `--ignore-non-visible` ¦ `-i`). 
