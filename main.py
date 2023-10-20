import get_index_permissions
import xml.etree.ElementTree as ET
import numpy as np
import joblib


def process(file_path):
    index_permission = get_index_permissions.get_index_permission()
    permissions = []
    for i in file_path:
        tree = ET.parse(i)
        root = tree.getroot()
        tmp = []
        for item in root.iter('uses-permission'):
            x = item.get("{http://schemas.android.com/apk/res/android}name")
            x = x.split('.')[-1]
            tmp.append(x)
        if len(tmp) > 0:
            permissions.append(tmp)

    intput_data = np.array([[0] * len(index_permission)] * (len(permissions)))

    for i in range(len(permissions)):
        for k in permissions[i]:
            index = index_permission[k]
            intput_data[i][index] = 1

    model_1 = joblib.load("Models/Random_Forest_Model_2.joblib")
    categories = ["SAFE", "NOT SAFE"]
    result = model_1.predict(intput_data)
    ans = []
    for i in result:
        ans.append(categories[i])
    return ans
