# -*- coding:utf-8 -*-

"""
 Verion: 1.0
 Author: zhangjian
 Site: https://iliangqunru.bitcron.com/
 File: pyeverything.py
 Time: 2018/3/9
 
 Add New Functional pyeverything.py
"""
import logging
import sys
from ctypes import windll, create_unicode_buffer, byref, WinDLL

level = logging.DEBUG
format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
datefmt = '%Y-%m-%d %H:%M'
logging.basicConfig(level=level, format=format, datefmt=datefmt)
logger = logging.getLogger(__name__)
PY3 = False

if sys.version > '3':
    PY3 = True


class BaseException(Exception):
    def __init__(self, *args, **kwargs):
        pass


class UnknownOSVersionException(BaseException):
    """UnknownOSVersion Exception"""
    pass


class UnknowOperationSystemException(BaseException):
    """UnknowOperationSystemException"""
    pass


from platform import architecture, platform

arch = architecture()
platform = platform()

logger.info("==> current os version is : (%s , %s)", platform, arch)


class Singleton(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance


class PyEverything(Singleton):
    def __init__(self):
        if not str(arch[1]).__contains__("Windows"):
            raise UnknowOperationSystemException("Unknown Operation System , And Only Apply For Windows")

        if str(arch[0]).__contains__("64"):
            self.everything_dll = windll.LoadLibrary(r'Everything64.dll')
        elif str(arch[0]).__contains__("32"):
            self.everything_dll = windll.LoadLibrary(r'Everything32.dll')
        else:
            raise UnknownOSVersionException("Unknown OS Version")

    def everything_clean_up(self) -> None:
        """The Everything_CleanUp function resets the result list and search state, freeing any allocated memory by the library."""
        self.everything_dll.Everything_CleanUp()

    @property
    def everything_delete_run_history(self) -> int:
        """
            The Everything_DeleteRunHistory function deletes all run history.Calling this function will clear all run history from memory and disk.
            Return Value:
            The function returns non-zero if run history is cleared.
            The function returns 0 if an error occurred. To get extended error information, call Everything_GetLastError

        """
        return self.everything_dll.Everything_DeleteRunHistory()

    @property
    def everything_get_last_error(self) -> int:
        """The Everything_GetLastError function retrieves the last-error code value."""
        return self.everything_dll.Everything_GetLastError()

    def everything_get_result_full_path_name_w(self, index: int, lp_string: str, n_max_count: int) -> None:
        """The Everything_GetResultFullPathName function retrieves the full path and file name of the visible result.
        index
            Zero based index of the visible result.
        lpString [out]
            Pointer to the buffer that will receive the text. If the string is as long or longer than the buffer, the string is truncated and terminated with a NULL character.
        nMaxCount
            Specifies the maximum number of characters to copy to the buffer, including the NULL character. If the text exceeds this limit, it is truncated.
        """
        self.everything_dll.Everything_GetResultFullPathNameW(index, lp_string, n_max_count)

    @property
    def everything_get_num_file_results(self) -> int:
        """The Everything_GetNumFileResults function returns the number of visible file results.
            返回文件数量
        """
        return self.everything_dll.Everything_GetNumFileResults()

    @property
    def everything_get_num_folder_results(self) -> int:
        """The Everything_GetNumFolderResults function returns the number of visible folder results.
            返回文件件数量
        """
        return self.everything_dll.Everything_GetNumFolderResults()

    @property
    def everything_get_num_results(self) -> int:
        """The Everything_GetNumResults function returns the number of visible file and folder results.
            结果数量，包含文件和文件夹
        """
        return self.everything_dll.Everything_GetNumResults()

    def everything_get_result_file_name(self, index: int):
        """The Everything_GetResultFileName function retrieves the file name part only of the visible result."""
        return self.everything_dll.Everything_GetResultFileNameW(index)

    # Manipulating the search state
    def everything_set_search_w(self, key_string: str) -> None:
        """The Everything_SetSearch function sets the search string for the IPC Query."""
        self.everything_dll.Everything_SetSearchW(key_string)

    def everything_set_match_path_w(self, enable: bool) -> None:
        """The Everything_SetMatchPath function enables or disables full path matching for the next call to
        Everything_Query. """
        self.everything_dll.Everything_SetMatchPath(enable)

    def everything_set_match_case(self, enable: bool = False) -> None:
        """The Everything_SetMatchCase function enables or disables full path matching for the next call to Everything_Query.
            搜素是否区分大小
            enable
            Specifies whether the search is case sensitive or insensitive.

            If this parameter is TRUE, the search is case sensitive.

            If the parameter is FALSE, the search is case insensitive.

        """
        self.everything_dll.Everything_SetMatchCase(enable)

    def everything_query_w(self, wait: bool = True) -> None:
        """The Everything_Query function executes an Everything IPC query with the current search state.
        wait

            Should the function wait for the results or return immediately.

            Set this to FALSE to post the IPC Query and return immediately.

            Set this to TRUE to send the IPC Query and wait for the results.
        """
        self.everything_dll.Everything_QueryW(wait)

    def __call__(self, *args, **kwargs):
        pass

    def __del__(self):
        self.everything_dll.Everything_CleanUp()


from typing import List, Dict, Any

FileList = List[str]
HookData = Dict[str, Any]


def magix(str_buffer_size: int = 512, only_first: bool = False, match_case: bool = False, query_wait: bool = True):
    """magic box"""

    def _decorator(func):
        def wrapper(self, *args, **kwargs):
            # 创建buffer
            str_buffer = create_unicode_buffer(str_buffer_size)
            # 搜索条件
            rs = func(self, *args, **kwargs)
            self.everything_set_match_case(match_case)
            # 调用搜索（核心）
            self.everything_query_w(query_wait)

            if only_first:
                self.everything_get_result_full_path_name_w(index=0, lp_string=byref(str_buffer),
                                                            n_max_count=len(str_buffer))
                return str_buffer.value

            def gen():
                for index in range(0, self.everything_get_num_results):
                    self.everything_get_result_full_path_name_w(index=index, lp_string=byref(str_buffer),
                                                                n_max_count=len(str_buffer))
                    yield str_buffer.value

            return [x for x in gen()]

        return wrapper

    return _decorator


class SearchFile(PyEverything):
    def __init__(self) -> None:
        super().__init__()

    @magix(str_buffer_size=100, )
    def common_search(self, key_string: str):
        """common search
            key_string  -> key file which you want to search in the disk
        """
        self.everything_set_search_w(key_string=key_string)

    @magix(match_case=True)
    def match_case_search(self, key_string):
        """是否区分大小写"""
        self.everything_set_search_w(key_string=key_string)
        pass

    # def registry_hooks(self, hooks: list, hook_data: dict, **kwargs) -> HookData:
    #     """hooks 注册"""
    #     hook_data = hook_data or dict()
    #     hooks = hooks or list()
    #     if hooks:
    #         for hook in hooks:
    #             _hook_data = hook(**kwargs)
    #             if _hook_data is not None:
    #                 # 将值返回出去
    #                 hook_data[hook.__name__] = _hook_data
    #     return hook_data
    #
    # d
    @property
    def files_search_nums(self) -> int:
        return self.everything_get_num_results

    @property
    def files_search_file_nums(self) -> int:
        return self.everything_get_num_file_results

    @property
    def files_search_folder_nums(self) -> int:
        return self.everything_get_num_folder_results


if __name__ == '__main__':
    search_file = SearchFile()
    # search_file.test_registry_hooks()
    common_search_rs = search_file.common_search(key_string="abc")
    print(len(common_search_rs))
    match_case_search_rs = search_file.match_case_search(key_string="abc")
    print(len(match_case_search_rs))
    # print(search_file.files_search_nums)
    # print(search_file.files_search_file_nums)
    # print(search_file.files_search_folder_nums)
