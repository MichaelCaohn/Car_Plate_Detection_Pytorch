import pandas as pd
import urllib.request

# read the entire file into a python array
with open('Indian_Number_plates.json', 'r') as f:
   data = f.readlines()

# remove the trailing "\n" from each line
data = map(lambda x: x.rstrip(), data)

# each element of 'data' is an individual JSON object.
# i want to convert it into an *array* of JSON objects
# which, in and of itself, is one large JSON object
# basically... add square brackets to the beginning
# and end, and have all the individual business JSON objects
# separated by a comma
data_json_str = "[" + ",".join(data) + "]"

# now, load it into pandas
data_df = pd.read_json(data_json_str)

# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
#    print(data_df["content"], data_df["annotation"])
#
count = 0
for index, row in data_df.iterrows():
    count = count + 1
    print(row["content"], row["annotation"])

    # labels = row["annotation"][0]["points"][0]["x"]
    # print(labels)
    print(row["annotation"][0]["points"][0]["x"], row["annotation"][0]["points"][0]["y"], row["annotation"][0]["points"][1]["x"], row["annotation"][0]["points"][1]["y"], row["annotation"][0]["imageWidth"], row["annotation"][0]["imageHeight"])
    name = row["content"].split("___")[1]

    print(name)
    times = 0
    times = name.count("jpeg") + name.count("jpg")
    write_train_times, write_val_times = 0, 0
    if count < 210:
        write_train_times = write_train_times + 1
        if times > 1:
            image_name = ((("car_data/images/train/" + name.replace(".jpeg", "")).replace(".png", ".jpg")).replace("JPG", "jpg")).replace("gif", "jpg")
        else:
            image_name = ((("car_data/images/train/" + name.replace(".jpeg", ".jpg")).replace(".png", ".jpg")).replace("JPG", "jpg")).replace("gif", "jpg")

        # if write_train_times == 1:
        #     f = open("car_data/training.txt", "w+")
        # else:
        f = open("car_data/training.txt", "a+")
        f.write(image_name + "\n")
        f.close()

        txt_name = image_name.replace("/images/", "/labels/").replace("jpg", "txt")
    else:
        write_val_times = write_val_times + 1
        if times > 1:
            image_name = ((("car_data/images/val/" + name.replace(".jpeg", "")).replace(".png", ".jpg")).replace("JPG", "jpg")).replace("gif", "jpg")
        else:
            image_name = ((("car_data/images/val/" + name.replace(".jpeg", ".jpg")).replace(".png", ".jpg")).replace("JPG", "jpg")).replace("gif", "jpg")

        # if write_train_times == 1:
        #     f = open("car_data/validation.txt", "w+")
        # else:
        f = open("car_data/validation.txt", "a+")
        f.write(image_name + "\n")
        f.close()

        txt_name = image_name.replace("/images/", "/labels/").replace("jpg", "txt")

    urllib.request.urlretrieve(row["content"], image_name)
    f = open(txt_name, "w+")
    f.write("1 "+ str(row["annotation"][0]["points"][0]["x"]) + " " + str(row["annotation"][0]["points"][0]["y"]) + " " + str(row["annotation"][0]["points"][1]["x"]) + " " + str(row["annotation"][0]["points"][1]["y"]))
    f.close()
# todo add a function to write all the path to picture in a txt file