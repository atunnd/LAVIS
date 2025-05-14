# """
#  Copyright (c) 2022, salesforce.com, inc.
#  All rights reserved.
#  SPDX-License-Identifier: BSD-3-Clause
#  For full license text, see the LICENSE file in the repo root or https://opensource.org/licenses/BSD-3-Clause
# """

# import os
# from pathlib import Path
# import zipfile


# from omegaconf import OmegaConf

# from lavis.common.utils import (
#     cleanup_dir,
#     download_and_extract_archive,
#     get_abs_path,
#     get_cache_path,
# )


# DATA_URL = {
#     "train": "../train2014.zip",  # md5: 0da8c0bd3d6becc4dcb32757491aca88
#     "val": "../val2014.zip",  # md5: a3d79f5ed8d289b7a7554ce06a5782b3
#     "test": "../test2014.zip",  # md5: 04127eef689ceac55e3a572c2c92f264
#     "test2015": "../test2015.zip",  # md5: 04127eef689ceac55e3a572c2c92f264
# }


# def download_datasets(root, url):
#     download_and_extract_archive(url=url, download_root=root, extract_root=storage_dir)

# def extract_local_zip(zip_path, extract_to):
#     print(f"Extracting {zip_path} to {extract_to}")
#     with zipfile.ZipFile(zip_path, 'r') as zip_ref:
#         zip_ref.extractall(extract_to)

# # if __name__ == "__main__":

# #     config_path = get_abs_path("configs/datasets/coco/defaults_cap.yaml")

# #     storage_dir = OmegaConf.load(
# #         config_path
# #     ).datasets.coco_caption.build_info.images.storage

# #     download_dir = Path(get_cache_path(storage_dir)).parent / "download"
# #     storage_dir = Path(get_cache_path(storage_dir))

# #     if storage_dir.exists():
# #         print(f"Dataset already exists at {storage_dir}. Aborting.")
# #         exit(0)


# #     print("ewewe")
# #     print(DATA_URL.items())
# #     for k, v in DATA_URL.items():
# #         print("Downloading {} to {}".format(v, k))
# #             #download_datasets(download_dir, v)
# #         extract_local_zip(v, k)

# #     # try:
# #     #     print("ewewe")
# #     #     print(DATA_URL.items())
# #     #     for k, v in DATA_URL.items():
# #     #         print("Downloading {} to {}".format(v, k))
# #     #         #download_datasets(download_dir, v)
# #     #         extract_local_zip(download_dir, storage_dir)
# #     # except Exception as e:
# #     #     # remove download dir if failed
# #     #     cleanup_dir(download_dir)
# #     #     print("Failed to download or extracting datasets. Aborting.")

# #     cleanup_dir(download_dir)

# if __name__ == "__main__":
#     # === SET storage_dir to "data" instead of reading config ===
#     storage_dir = Path("data")
#     storage_dir.mkdir(parents=True, exist_ok=True)

#     download_dir = storage_dir / "download"
#     download_dir.mkdir(parents=True, exist_ok=True)

#     if storage_dir.exists() and any(storage_dir.iterdir()):
#         print(f"Dataset already exists at {storage_dir}. Aborting.")
#         exit(0)

#     try:
#         for k, v in DATA_URL.items():
#             print(f"Downloading {v} to {k}")
#             download_datasets(download_dir, v)
#     except Exception as e:
#         cleanup_dir(download_dir)
#         print("Failed to download or extract datasets. Aborting.")
#         print(str(e))

#     cleanup_dir(download_dir)

import os
from pathlib import Path
from omegaconf import OmegaConf
from lavis.common.utils import (
    cleanup_dir,
    download_and_extract_archive,
    get_abs_path,
    get_cache_path,
)

# URLs của COCO dataset
# DATA_URL = {
#     "train": "http://images.cocodataset.org/zips/train2014.zip",
#     "val": "http://images.cocodataset.org/zips/val2014.zip",
#     "test": "http://images.cocodataset.org/zips/test2014.zip",
#     "test2015": "http://images.cocodataset.org/zips/test2015.zip",
# }

DATA_URL = {
    "test": "http://images.cocodataset.org/zips/test2014.zip",
    "test2015": "http://images.cocodataset.org/zips/test2015.zip",
}


# Override đường dẫn cache mặc định thành "data"
def get_cache_path(rel_path):
    return os.path.expanduser(os.path.join("data", rel_path))


def get_abs_path(rel_path):
    return os.path.join("lavis", rel_path)


def download_datasets(root, url):
    download_and_extract_archive(url=url, download_root=root, extract_root=storage_dir)


if __name__ == "__main__":
    # Load config
    config_path = get_abs_path("configs/datasets/coco/defaults_cap.yaml")
    config = OmegaConf.load(config_path)

    # Ghi đè đường dẫn lưu trữ vào "data/coco/images"
    config.datasets.coco_caption.build_info.images.storage = "coco/images"

    # Xây dựng đường dẫn lưu
    storage_dir = Path(get_cache_path(config.datasets.coco_caption.build_info.images.storage))
    download_dir = storage_dir.parent / "download"

    # Nếu thư mục đã tồn tại thì không làm lại
    if storage_dir.exists() and any(storage_dir.iterdir()):
        print(f"Dataset already exists at {storage_dir}. Aborting.")
        exit(0)

    try:
        for k, v in DATA_URL.items():
            print("Downloading {} to {}".format(v, k))
            download_datasets(download_dir, v)
    except Exception as e:
        cleanup_dir(download_dir)
        print(f"Failed to download or extract datasets: {e}. Aborting.")
        exit(1)

    # Cleanup thư mục tạm sau khi hoàn thành
    cleanup_dir(download_dir)
    print("Done.")

