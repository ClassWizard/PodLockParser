#!/usr/bin/python
# -*- coding: UTF-8 -*-

import yaml
import sys

def main():

    if get_file_path() is None:
        print("Error: 没有传入文件路径，请传入podfile.lock文件路径（拖入即可）")
        exit(0)

    result = parse_podfile(get_file_path())
    if result is None:
        exit(0)

    # # 初始化count字典
    # names = result[1]
    count_dict = {}
    # for name in names:
    #     count_dict[name] = 0

    # 填入数据
    pods = result[0]
    # print(pods)

    for top_level in pods:
        if isinstance(top_level, dict):
            if len(top_level.keys()) > 0:
                name = get_pod_name(list(top_level.keys())[0])
                # print('pod:' + name)
                add_count(name, count_dict)

                second_level = get_any_value(top_level)
                for libs in second_level:
                    name = get_pod_name(libs)
                    add_count(name, count_dict)
        elif isinstance(top_level, str):
            name = get_pod_name(top_level)
            # print('pod:' + name)
            add_count(name, count_dict)
        else:
            print("类型错误")

    print("----------- Dependency Count -----------")
    # 排序
    sorted_list = sorted(count_dict.items(), key=lambda x: (x[1]), reverse=True)
    # sorted_list = sorted(count_dict.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
    for tuple in sorted_list:
        print("%s: %d" % (tuple[0], tuple[1]))
    exit(1)

def parse_podfile(file_path):
    try:
        file_data = open(file_path)

    except IOError:
        print('Error: 没有找到文件或读取文件失败,File:(' + file_path + '）')
        return None
    else:
        # 解析文件
        pod_file = yaml.load(file_data, yaml.FullLoader)
        if isinstance(pod_file, dict) == False:
            print('Error: Podfile.lock解析失败,File:(' + file_path + '）')
            return None
        if 'DEPENDENCIES' not in pod_file:
            print('Error: Podfile.lock解析失败,File:(' + file_path + '）')
            return None
        if 'PODS' not in pod_file:
            print('Error: Podfile.lock解析失败,File:(' + file_path + '）')
            return None
        dependencies = pod_file['DEPENDENCIES']

        # 准备返回值
        pods = pod_file['PODS']
        lib_name_list = []
        result = (pods, lib_name_list)
        # 填充结果
        for dependency in dependencies:
            # print(dependency)
            # print(get_pod_name(dependency))
            lib_name_list.append(get_pod_name(dependency))


        file_data.close()

        return result

def get_any_value(dictionary):
    if isinstance(dictionary,dict) == False:
        return None
    if len(dictionary.keys()) <= 0:
        return None
    keys = dictionary.keys()
    key = list(keys)[0]
    return dictionary[key]

def get_pod_name(dependency):
    vs = dependency.split(' ')
    return vs[0]

def add_count(key, count_dict):
    if key in count_dict:
        count = count_dict[key]
        count_dict[key] = count + 1
    else:
        count_dict[key] = 1

def get_file_path():
    if len(sys.argv) > 1:
        return sys.argv[1]
    else:
        return None

if __name__ == '__main__':
    main()
