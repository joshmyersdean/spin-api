import matplotlib.pyplot as plt
from pycocotools.coco import COCO
from pycocotools import mask as maskUtils
import requests
import os
from PIL import Image
from typing import Dict, List, Union
from .types import Entry
from .object_mapping import file_to_object_mapping
from .exceptions import InitialRequestError
from .helpers import unzip_file
import numpy as np
import cv2
from tqdm import tqdm


class SPIN:
    def __init__(
        self,
        annotation_dir: str,
        image_dir: str,
        split: str = "test",
        download: bool = False,
    ) -> None:
        """
        Initialize the SPINViewer with annotations and image directories.

        :param annotation_dir: Directory containing	annotation files.
        :param image_dir: Directory	containing images.
        :param split: Dataset split, e.g., "train",	"test".	Default	is "test".
        :param download: Download data.
        """
        if download:
            self.download_spin(save_directory=annotation_dir)
        self.wholes: COCO = COCO(f"{annotation_dir}/spin_{split}_wholes.json")
        self.parts: COCO = COCO(f"{annotation_dir}/spin_{split}_parts.json")
        self.subparts: COCO = COCO(f"{annotation_dir}/spin_{split}_subparts.json")

        self.split: str = split
        self.image_dir: str = image_dir
        self.cocos: List[COCO] = [self.wholes, self.parts, self.subparts]
        self.num_cocos: int = len(self.cocos)

    def get_image(self, image_id: int) -> Image.Image:
        """
        Get	the	image corresponding	to the given image ID.

        :param image_id: ID	of the image to	retrieve.
        :return: PIL Image object.
        """
        image_info: Dict[str, Union[str, int]] = self.subparts.loadImgs(image_id)[0]
        fname: str = image_info["file_name"]
        image_path: str = f"{self.image_dir}/{self.split}/{fname}.JPEG"
        return Image.open(image_path).convert("RGB")

    def getImgIds(self) -> List[int]:
        """
        Get	a list of all image	IDs.

        :return: List of image IDs.
        """
        return self.subparts.getImgIds()

    def get_object_name_for_file(self, img_id: int) -> str:
        """
        Get	the	object name	corresponding to the given image ID.

        :param img_id: ID of the image.
        :return: Object	name.
        """
        image_info: Dict[str, Union[str, int]] = self.subparts.loadImgs(img_id)[0]
        fname: str = image_info["file_name"]
        return file_to_object_mapping[fname]

    def get_categories(
        self, granularity: str = "subpart", verbose: bool = False
    ) -> Dict[int, Entry]:
        """
        Get	the	categories for a given granularity level.

        :param granularity:	Level of granularity ("subpart", "part", "whole"). Default is "subpart".
        :param verbose:	If True, prints	additional information.	Default	is False.
        :return: Dictionary	of categories.
        :raises	NotImplementedError: If	the	granularity	is not supported.
        """
        if granularity == "subpart":
            return self.subparts.cats
        elif granularity == "part":
            return self.parts.cats
        elif granularity == "whole":
            return self.wholes.cats
        else:
            raise NotImplementedError(
                "Only supports granularity in {subpart,	part, whole}"
            )

    def display_annotations(
        self, image_id: int, fig_size: List[int] = [30, 20], draw_bbox: bool = False
    ) -> None:
        """
        Display	annotations	for	a given	image ID.

        :param image_id: ID	of the image to	display.
        :param fig_size: Size of the figure	to display.	Default	is [30,	20].
        :param draw_bbox: If True, draw	bounding boxes.	Default	is False.
        """
        plt.rcParams["figure.figsize"] = fig_size

        image: Image.Image = self.get_image(image_id)

        cols: int = 3
        rows: int = 1
        names: List[str] = ["Whole", "Part", "Subpart"]
        for index, coco in enumerate(self.cocos, start=1):
            plt.subplot(rows, cols, index)
            plt.axis("off")
            plt.title(f"{names[index-1]}")
            plt.imshow(image)
            anns: List[int] = coco.getAnnIds(imgIds=image_id)
            loaded_anns: List[Dict[str, Union[str, int]]] = coco.loadAnns(anns)
            coco.showAnns(loaded_anns, draw_bbox=draw_bbox)

        plt.show()

    def rasterize_coco_segmentations(
        self, coco: COCO, image_id: int, background_class: int
    ) -> np.ndarray:
        """
        Rasterizes COCO	segmentations for a	specified image, allowing the user to specify which	class is the background.

        :param coco: COCO object containing	the	dataset	annotations.
        :param image_id: ID	of the image to	rasterize segmentations	for.
        :param background_class: Class ID to be	used as	the	background.
        :return: A 2D numpy	array with the same	dimensions as the image, where each	pixel value	represents the class ID.
        """
        img_info = coco.loadImgs(image_id)[0]
        height, width = img_info["height"], img_info["width"]

        segmentation_map = np.full((height, width), background_class, dtype=np.uint8)

        ann_ids = coco.getAnnIds(imgIds=image_id)
        anns = coco.loadAnns(ann_ids)

        for ann in anns:
            class_id = ann["category_id"]
            mask = maskUtils.decode(ann["segmentation"])
            segmentation_map[mask > 0] = class_id

        return segmentation_map

    def rasterize_dataset(self, save_path: str = "spin_dataset/annotations") -> None:
        """
        Rasterizes COCO	segmentations for a	specified split	for	all	granularities.

        :param save_path: Where	to save	annotations.
        """

        os.makedirs(os.path.join(save_path, f"{self.split}_subpart"), exist_ok=True)
        os.makedirs(os.path.join(save_path, f"{self.split}_part"), exist_ok=True)
        os.makedirs(os.path.join(save_path, f"{self.split}_whole"), exist_ok=True)
        for im_id in tqdm(self.getImgIds()):
            image_info: Dict[str, Union[str, int]] = self.subparts.loadImgs(im_id)[0]
            fname: str = image_info["file_name"]
            raster_sub: np.ndarray = self.rasterize_coco_segmentations(
                self.subparts, im_id, background_class=0
            )
            raster_part: np.ndarray = self.rasterize_coco_segmentations(
                self.parts, im_id, background_class=40
            )
            raster_whole: np.ndarray = self.rasterize_coco_segmentations(
                self.wholes, im_id, background_class=158
            )

            sub_path: str = os.path.join(
                save_path, f"{self.split}_subpart", f"{fname}.png"
            )
            part_path: str = os.path.join(
                save_path, f"{self.split}_part", f"{fname}.png"
            )
            whole_path: str = os.path.join(
                save_path, f"{self.split}_whole", f"{fname}.png"
            )

            cv2.imwrite(sub_path, raster_sub)
            cv2.imwrite(part_path, raster_part)
            cv2.imwrite(whole_path, raster_whole)

    def download_spin(
        self,
        link: str = "https://joshmyersdean.github.io/spin/spin_coco.zip",
        save_directory: str = "spin_jsons",
        save_name: str = "spin.zip",
    ) -> None:
        """
        Downloads a	file using a shared	link.

        :param sharepoint_link:	The	shared link	URL	to the file.
        :param save_directory: The directory where the file	should be saved.
        :param save_name: The name to save the file	as.
        :return: None.
        """
        os.makedirs(save_directory, exist_ok=True)
        headers: str = {
            "User-Agent": "Mozilla/5.0 (Windows	NT 10.0; Win64;	x64) AppleWebKit/537.36	(KHTML,	like Gecko)	Chrome/91.0.4472.124 Safari/537.36"
        }
        res = requests.get(link, allow_redirects=False, headers=headers)
        if res.status_code != 200:
            raise InitialRequestError(res.status_code)

        file_path = os.path.join(save_directory, save_name)
        with open(file_path, "wb") as file:
            for chunk in res.iter_content(1024):
                file.write(chunk)

        print(f"File downloaded	successfully and saved to {file_path}")
        unzip_file(zip_path=file_path, extract_to=save_directory)
