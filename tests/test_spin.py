import pytest
import os
import shutil
import numpy as np
from pycocotools.coco import COCO
from PIL import Image
from spin.spin import SPIN, InitialRequestError
from spin.helpers import unzip_file
import zipfile


@pytest.fixture(scope="module")
def setup_spin():
    annotation_dir = "test_annotations"
    image_dir = "test_images"
    split = "test"
    spin = SPIN(annotation_dir, image_dir, split, download=True)

    # Create test directories
    os.makedirs(annotation_dir, exist_ok=True)
    os.makedirs(image_dir, exist_ok=True)
    os.makedirs(f"{image_dir}/{split}", exist_ok=True)

    # Create dummy annotation files
    with open(f"{annotation_dir}/spin_{split}_wholes.json", "w") as f:
        f.write("{}")
    with open(f"{annotation_dir}/spin_{split}_parts.json", "w") as f:
        f.write("{}")
    with open(f"{annotation_dir}/spin_{split}_subparts.json", "w") as f:
        f.write("{}")

    # Create dummy image file
    image = Image.new("RGB", (100, 100))
    image.save(f"{image_dir}/{split}/dummy_image.JPEG")

    yield spin

    # Cleanup after tests
    shutil.rmtree(annotation_dir)
    shutil.rmtree(image_dir)


def test_download_spin(setup_spin):
    spin = setup_spin
    save_directory = "test_spin_jsons"
    save_name = "spin.zip"

    # Ensure the save directory is cleaned up
    if os.path.exists(save_directory):
        shutil.rmtree(save_directory)

    # Test download_spin with a dummy link (replace with actual URL if needed)
    with pytest.raises(InitialRequestError):
        spin.download_spin(
            link="https://joshmyersdean.github.io/spin/spin_coco2.zip",
            save_directory=save_directory,
            save_name=save_name,
        )

    # Clean up
    if os.path.exists(save_directory):
        shutil.rmtree(save_directory)


def test_rasterize_coco_segmentations(setup_spin):
    spin = setup_spin
    image_id = 0  # Dummy image ID
    background_class = 0

    # Create dummy COCO object
    coco = COCO()
    coco.dataset = {
        "images": [{"id": image_id, "width": 100, "height": 100}],
        "annotations": [],
        "categories": [],
    }
    coco.createIndex()

    segmentation_map = spin.rasterize_coco_segmentations(
        coco, image_id, background_class
    )
    assert segmentation_map.shape == (100, 100)
    assert np.all(segmentation_map == background_class)


def test_unzip_file():
    # Create a dummy zip file
    dummy_zip_path = "dummy.zip"
    dummy_extract_dir = "dummy_extracted"
    os.makedirs(dummy_extract_dir)
    with zipfile.ZipFile(dummy_zip_path, "w") as zipf:
        zipf.writestr(f"{dummy_extract_dir}/dummy.txt", "This is a test file.")

    # Test unzip_file
    unzip_file(dummy_zip_path, extract_to=dummy_extract_dir)
    assert os.path.exists(os.path.join(dummy_extract_dir, "dummy.txt"))

    # Clean up
    os.remove(dummy_zip_path)
    shutil.rmtree(dummy_extract_dir)
