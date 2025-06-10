# ngretrieve ⤵️
Script to retrieve a crop based on annotations in a Neuroglancer state (either the URL or the JSON file). Works with either a point cloud, or one or several lines/bounding boxes.

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
python download_from_points.py --url 'https://neuroglancer-demo.appspot.com/#!...' --volume_layer_name "layer1" --bbox_layer_name "layer2" [--output_dir '/path/to/output/'] [--margin 50] [--log]
```

```bash
python download_from_points.py --json '/path/to/state.json' --volume_layer_name "layer1" --bbox_layer_name "layer2" [--output_dir '/path/to/output/'] [--margin 50] [--log]
```
