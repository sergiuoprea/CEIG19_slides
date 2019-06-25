import csv

import numpy as np

def generate_time_per_object (data, objects, groups):

    time_per_object_ = np.zeros((len(groups), len(objects)), dtype=float)
    counts_per_object_ = np.zeros((len(groups), len(objects)), dtype=int)

    for _entry in data:

        object_ = objects.index(_entry["object"])
        group_ = groups.index(_entry["group"])
        time_ = _entry["time"]

        time_per_object_[group_, object_] += time_
        counts_per_object_[group_, object_] += 1

    for i in range(time_per_object_.shape[0]):
        for j in range(time_per_object_.shape[1]):
            time_per_object_[i, j] /= counts_per_object_[i, j]

    with open("time_per_object_overall.dat", "w") as _f:

        _f.write("object ")
        for _g in groups:
            _f.write(_g + " ")
        _f.write("\n")

        for _o in objects:
            index_o_ = objects.index(_o)
            _f.write("{0} ".format(index_o_))
            for _g in groups:
                index_g_ = groups.index(_g)
                _f.write("{:5f} ".format(time_per_object_[index_g_, index_o_]))
            _f.write("\n")

def generate_accuracy_per_object (data, objects, groups, limit= 25):

    accuracy_per_object_ = np.zeros((len(groups), len(objects)), dtype=float)
    counts_per_object_ = np.zeros((len(groups), len(objects)), dtype=float)

    for _entry in data:

        object_ = objects.index(_entry["object"])
        group_ = groups.index(_entry["group"])
        errors_ = _entry["errors"]

        for _error in errors_:
            if errors_[_error] != 0.0 and np.abs(errors_[_error]) < limit:
                accuracy_per_object_[group_, object_] += np.abs(errors_[_error])
                counts_per_object_[group_, object_] += 1

    for i in range(accuracy_per_object_.shape[0]):
        for j in range(accuracy_per_object_.shape[1]):
            print(accuracy_per_object_[i, j] / counts_per_object_[i, j])
            accuracy_per_object_[i, j] /= counts_per_object_[i, j]

    with open("accuracy_per_object_overall.dat", "w") as _f:

        _f.write("object ")
        for _g in groups:
            _f.write(_g + " ")
        _f.write("\n")

        for _o in objects:
            index_o_ = objects.index(_o)
            _f.write("{0} ".format(index_o_))
            for _g in groups:
                index_g_ = groups.index(_g)
                _f.write("{:5f} ".format(accuracy_per_object_[index_g_, index_o_]))
            _f.write("\n")

def get_data(fileName):

    with open(fileName) as _f:

        csv_ = csv.DictReader(_f, delimiter=";")
        headers_ = csv_.fieldnames

        print(headers_)

        groups_ = []
        objects_ = []
        data_ = []

        for _e in csv_:

            entry_ = {}
            entry_["user"] = _e["UserId"]
            entry_["group"] = _e["GroupId"]
            entry_["hand"] = _e["Hand"]
            entry_["object"] = _e["Object"]

            entry_["errors"] = {}
            errors_ = _e["Errors"].strip().split(" ")
            for _error in errors_:
                _error = _error.split(":")
                entry_["errors"][_error[0]] = float(_error[1])

            entry_["time"] = float(_e["Time"])

            data_.append(entry_)

            if _e["GroupId"] not in groups_:
                groups_.append(_e["GroupId"])

            if _e["Object"] not in objects_:
                objects_.append(_e["Object"])
        
        return data_, objects_, groups_

if __name__ == "__main__":

    DATA_, OBJECTS_, GROUPS_ = get_data("csvs/data_overall.csv")
    print(OBJECTS_)
    print(GROUPS_)
    generate_time_per_object(DATA_, OBJECTS_, GROUPS_)
    generate_accuracy_per_object(DATA_, OBJECTS_, GROUPS_)


# TO SERGIU:
# OBJECT ID 072-a_toy_airplane is bad
# REMOVE TRAILING SPACE FROM ERROR STRING