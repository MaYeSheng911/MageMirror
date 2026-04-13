import os
from ai.image_processor import process_image

UPLOAD_DIR = "/home/ubuntu/MageMirror/uploads"

def batch_process():

    files = os.listdir(UPLOAD_DIR)

    count = 0

    for file in files:

        if file.endswith(".jpg") or file.endswith(".jpeg"):

            file_path = os.path.join(
                UPLOAD_DIR,
                file
            )

            try:

                new_path = process_image(file_path)

                print("Processed:", new_path)

                count += 1

            except Exception as e:

                print("Error:", file, e)

    print("Total processed:", count)


if __name__ == "__main__":

    batch_process()
