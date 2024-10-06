import yaml
import os
from conf.setting import FILE_PATH


def get_testcase_yaml(file):
    """
    读取 YAML 文件并返回数据
    :param file: YAML 文件路径
    :return 文件内容
    """
    try:
        with open(file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)  # 使用 safe_load 读取数据
            return data  # 返回读取的数据
    except Exception as e:
        print(f"Error reading YAML file: {e}")
        return None


class ReadYamlData:
    def __init__(self, file=None):
        if file is None:
            self.file = 'login.yaml'
        else:
            self.file = file

    def _write_yaml(self, file_path, data, mode):
        with open(file_path, mode, encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True) # 设置allow_unicode = False，为正确显示中文

    def write_yaml_data(self, data):
        file_path = FILE_PATH['extract']
        mode = 'w' if not os.path.exists(file_path) else 'a'
        self._write_yaml(file_path, data, mode)

    def get_extract_yaml(self, node_name):
        """读取接口提取的变量值

        Args:
            node_name: extract.yaml文件中的key
        """
        file_path = FILE_PATH['extract']
        if not os.path.exists(file_path):
            print('extract.yaml文件不存在')
            file = open(file_path, 'w', encoding='utf-8')
            file.close()
            print('extract.yaml文件已创建')

        with open(file_path, 'r', encoding='utf-8') as f:
            extract_data = yaml.safe_load(f)
            return extract_data[node_name]


if __name__ == '__main__':
    print(get_testcase_yaml(FILE_PATH['extract']))
