import re

from common import debugtalk
from common.read_yaml import ReadYamlData, get_testcase_yaml
import json
from common.debugtalk import DebugTalk


class BaseRequests:
    def __init__(self):
        self.read = ReadYamlData()

    def replace_load(self, data):
        """替换yaml 文件解析有${}的参数
        """
        str_data = data
        if not isinstance(data, str):
            str_data = json.dumps(data, ensure_ascii=False)

        for i in range(str_data.count('${')):
            if '${' in str_data and '}' in str_data:
                start_index = str_data.index('$')
                end_index = str_data.index('}', start_index)
                ref_all_params = str_data[start_index:end_index + 1]
                # 取出函数名
                func_name = ref_all_params[2:ref_all_params.index('(')]
                # 取出参数
                params = ref_all_params[ref_all_params.index('(') + 1:ref_all_params.index(')')]

                # 执行函数
                extract_data = getattr(DebugTalk(), func_name)(*params.split(',') if params else '')

                # 替换
                str_data = str_data.replace(ref_all_params, str(extract_data))

        if data and isinstance(data, dict):
            data = json.loads(str_data)
        else:
            data = str_data

        return data

    def replace_placeholder(data):
        """用实际值替换数据中的占位符。"""
        pattern = re.compile(r"\$\{(\w+)(\((.*?)\))?}")
        if isinstance(data, dict):
            data_str = str(data)
        else:
            data_str = data

        matches = pattern.findall(data_str)
        for func_name, _, args in matches:
            func = getattr(debugtalk, func_name, None)
            if func:
                if args:
                    args_list = [arg.strip() for arg in args.split(',')]
                    value = func(*args_list)
                else:
                    value = func()
                placeholder = f"${{{func_name}({args})}}"
                data_str = data_str.replace(placeholder, f'"{value}"')
        return eval(data_str)

    def send_request(self):
        pass


if __name__ == '__main__':
    data = get_testcase_yaml('../testcase/Login/login.yaml')

    base = BaseRequests()
    print(base.replace_load(data))
