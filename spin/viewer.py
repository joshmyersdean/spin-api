import matplotlib.pyplot as plt
from pycocotools.coco import COCO
import json
from PIL import Image
from typing import Dict, List, Union
from .types import Entry
from .object_mapping import file_to_object_mapping


class SPINViewer:
    def __init__(
        self,
        annotation_dir: str,
        image_dir: str,
        split: str = "test",
    ) -> None:
        """
        Initialize the SPINViewer with annotations and image directories.

        :param annotation_dir: Directory containing annotation files.
        :param image_dir: Directory containing images.
        :param split: Dataset split, e.g., "train", "test". Default is "test".
        """
        self.wholes: COCO = COCO(f"{annotation_dir}/spin_{split}_wholes.json")
        self.parts: COCO = COCO(f"{annotation_dir}/spin_{split}_parts.json")
        self.subparts: COCO = COCO(f"{annotation_dir}/spin_{split}_subparts.json")

        self.split: str = split
        self.image_dir: str = image_dir
        self.cocos: List[COCO] = [self.wholes, self.parts, self.subparts]
        self.num_cocos: int = len(self.cocos)

    def get_image(self, image_id: int) -> Image.Image:
        """
        Get the image corresponding to the given image ID.

        :param image_id: ID of the image to retrieve.
        :return: PIL Image object.
        """
        image_info: Dict[str, Union[str, int]] = self.subparts.loadImgs(image_id)[0]
        fname: str = image_info["file_name"]
        image_path: str = f"{self.image_dir}/{self.split}/{fname}.JPEG"
        return Image.open(image_path).convert("RGB")

    def getImgIds(self) -> List[int]:
        """
        Get a list of all image IDs.

        :return: List of image IDs.
        """
        return self.subparts.getImgIds()

    def get_object_name_for_file(self, img_id: int) -> str:
        """
        Get the object name corresponding to the given image ID.

        :param img_id: ID of the image.
        :return: Object name.
        """
        image_info: Dict[str, Union[str, int]] = self.subparts.loadImgs(img_id)[0]
        fname: str = image_info["file_name"]
        return file_to_object_mapping[fname]

    def get_categories(
        self, granularity: str = "subpart", verbose: bool = False
    ) -> Dict[int, Entry]:
        """
        Get the categories for a given granularity level.

        :param granularity: Level of granularity ("subpart", "part", "whole"). Default is "subpart".
        :param verbose: If True, prints additional information. Default is False.
        :return: Dictionary of categories.
        :raises NotImplementedError: If the granularity is not supported.
        """
        if granularity == "subpart":
            return self.subparts.cats
        elif granularity == "part":
            return self.parts.cats
        elif granularity == "whole":
            return self.wholes.cats
        else:
            raise NotImplementedError(
                "Only supports granularity in {subpart, part, whole}"
            )

    def display_annotations(
        self, image_id: int, fig_size: List[int] = [30, 20], draw_bbox: bool = False
    ) -> None:
        """
        Display annotations for a given image ID.

        :param image_id: ID of the image to display.
        :param fig_size: Size of the figure to display. Default is [30, 20].
        :param draw_bbox: If True, draw bounding boxes. Default is False.
        """
        plt.rcParams["figure.figsize"] = fig_size

        image: Image.Image = self.get_image(image_id)

        cols: int = 3
        rows: int = (self.num_cocos + cols - 1) // cols

        for index, coco in enumerate(self.cocos, start=1):
            plt.subplot(rows, cols, index)
            plt.axis("off")
            plt.imshow(image)
            anns: List[int] = coco.getAnnIds(imgIds=image_id)
            loaded_anns: List[Dict[str, Union[str, int]]] = coco.loadAnns(anns)
            coco.showAnns(loaded_anns, draw_bbox=draw_bbox)

        plt.show()
