from glob import glob
import shutil
import random
import os

individuals = glob("instructor_utils/original/*")

random.shuffle(individuals)


for individual in individuals[:500]:
    print(individual)

    try:
        os.makedirs(f"instructor_utils/probe/{individual.split('/')[-1]}", exist_ok=True)
        os.makedirs(f"instructor_utils/multi_image_gallery/{individual.split('/')[-1]}", exist_ok=True)
        print("Directory '%s' created successfully" % individual.split('/')[-1])
    except OSError as error:
        print("Directory '%s' can not be created")

    

    filenames = glob(f"instructor_utils/original/{individual.split('/')[-1]}/*.jpg")

    for filename in filenames[:200]:
        if "001.jpg" in filename:
            shutil.copy(filename, filename.replace("original", "probe").replace("001.jpg", "002.jpg"), )
        elif "002.jpg" in filename:
            shutil.copy(filename, filename.replace("original", "multi_image_gallery").replace("002.jpg", "001.jpg"), )
        elif "003.jpg" in filename:
            shutil.copy(filename, filename.replace("original", "multi_image_gallery").replace("003.jpg", "002.jpg"), )
        elif "004.jpg" in filename:
            shutil.copy(filename, filename.replace("original", "multi_image_gallery").replace("004.jpg", "003.jpg"), )
        elif "005.jpg" in filename:
            shutil.copy(filename, filename.replace("original", "multi_image_gallery").replace("005.jpg", "004.jpg"), )
        elif "006.jpg" in filename:
            shutil.copy(filename, filename.replace("original", "multi_image_gallery").replace("006.jpg", "005.jpg"), )
        elif "007.jpg" in filename:
            shutil.copy(filename, filename.replace("original", "multi_image_gallery").replace("007.jpg", "006.jpg"), )
        elif "008.jpg" in filename:
            shutil.copy(filename, filename.replace("original", "multi_image_gallery").replace("008.jpg", "007.jpg"), )
        elif "009.jpg" in filename:
            shutil.copy(filename, filename.replace("original", "multi_image_gallery").replace("009.jpg", "008.jpg"), )
        elif "010.jpg" in filename:
            shutil.copy(filename, filename.replace("original", "multi_image_gallery").replace("010.jpg", "009.jpg"), )
        elif "011.jpg" in filename:
            shutil.copy(filename, filename.replace("original", "multi_image_gallery").replace("011.jpg", "010.jpg"), )
