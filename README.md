# ngretrieve ⤵️
Script to retrieve a crop

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
python download_from_bbox.py --url 'https://neuroglancer-demo.appspot.com/#!...' --volume_layer_name "layer1" --bbox_layer_name "layer2" [--output_dir '/path/to/output/'] [--margin 50] [--log]
```

```bash
python download_from_bbox.py --json '/path/to/state.json' --volume_layer_name "layer1" --bbox_layer_name "layer2" [--output_dir '/path/to/output/'] [--margin 50] [--log]
```
