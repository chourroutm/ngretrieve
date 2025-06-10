import argparse

import neuroglancer
import neuroglancer.cli
import numpy as np
import cloudvolume
import re

def _legacy_source_url(source_url):
    # see https://github.com/seung-lab/cloud-volume/discussions/653
    match = re.match(r'^(.*)\|(.*)\:$', source_url)
    if match:
        protocol_url = match.group(1)
        pipe_format = match.group(2)
        if pipe_format == "neuroglancer-precomputed":
            pipe_format = "precomputed"
        if pipe_format == "zarr2":
            pipe_format = "zarr"
        source_url =  f"{pipe_format}://{protocol_url}"
        print(source_url)
    return source_url

def retrieve_from_state(state: neuroglancer.ViewerState, volume_layer_name: str = "", annotation_layer_name: str = "") -> tuple[str, cloudvolume.Bbox]:
    volume_layer = state.layers[volume_layer_name]
    if not isinstance(volume_layer.layer, neuroglancer.ImageLayer) and not isinstance(volume_layer.layer, neuroglancer.SegmentationLayer):
        raise Exception("Wrong type for volume layer")
    
    annotation_layer = state.layers[annotation_layer_name]
    if not isinstance(annotation_layer.layer, neuroglancer.AnnotationLayer):
        raise Exception("Wrong type for annotation layer")
    all_points = []
    for current_annotation in annotation_layer.annotations:
        if isinstance(current_annotation, neuroglancer.PointAnnotation):
            all_points.append(current_annotation.point)
        elif isinstance(current_annotation, neuroglancer.LineAnnotation) or isinstance(current_annotation, neuroglancer.AxisAlignedBoundingBoxAnnotation):
            all_points.append(current_annotation.point_a)
            all_points.append(current_annotation.point_b)
    bounding_box = cloudvolume.Bbox.from_points(all_points)
    return _legacy_source_url(volume_layer.layer.source[0].url), bounding_box

def download_from_bbox(output_dir: str, volume_source_url: str, bounding_box: cloudvolume.Bbox, margin = 0):
    if margin > 0:
        bounding_box = bounding_box.adjust(margin)
    
    vol = cloudvolume.CloudVolume(volume_source_url, parallel=True, progress=True, use_https=True)

    vol_crop = vol.download(bounding_box, mip=0, parallel=1) # fancy Numpy array
    
    return vol_crop.save_images(directory=output_dir, image_format="TIFF", global_norm=False)

def main(args=None):
    ap = argparse.ArgumentParser()
    neuroglancer.cli.add_state_arguments(ap, required=True)
    ap.add_argument("--log", "-l", action="store_true", help="Print log")
    ap.add_argument("--output_dir", "-o", type=str, default=".", help="Output directory for saved slices")
    ap.add_argument("--volume_layer_name", "-v", "--volume", type=str, default="", help="Volume layer")
    ap.add_argument("--annotation_layer_name", "-a", "-p", "--points", type=str, default="", help="Annotation layer with point cloud")
    ap.add_argument("--margin", "-m", type=int, default=0, help="Margin around the bounding box")
    parsed_args = ap.parse_args()
    if parsed_args.log:
        print(parsed_args.state)
    volume_source_url, bounding_box = retrieve_from_state(
        state=parsed_args.state, 
        volume_layer_name=parsed_args.volume_layer_name,
        annotation_layer_name=parsed_args.annotation_layer_name,
        )
    if parsed_args.log:
        print(volume_source_url)
        print(bounding_box.to_filename())
        if parsed_args.margin > 0:
            print(f"Note: a margin of {parsed_args.margin} was then applied.")
    output_dir = download_from_bbox(
        output_dir=parsed_args.output_dir,
        volume_source_url=volume_source_url,
        bounding_box=bounding_box,
        margin=parsed_args.margin
    )
    if parsed_args.log:
        print(output_dir)

if __name__ == "__main__":
    main()
