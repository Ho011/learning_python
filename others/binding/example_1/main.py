from ctypes import *
from typing import (
    List,
    Any,
    Union
)
from functools import wraps
from pathlib import Path

path = Path(__file__).parent / 'test.so'
lib = cdll.LoadLibrary(str(path))

def wrap_function(funcname: str, argtypes: List[Any]= None, restype: Any= None):
    func = lib.__getattr__(funcname)
    func.argtypes = argtypes
    func.restype = restype
    return func

def to_byte_str(string: str):
    string = str(string)
    return string.encode('utf-8', 'ignore')

func = wrap_function('func')
sum_cpp = wrap_function('sum', [c_int, c_int], c_int)
# func()
# print(sum_cpp(1 , 200))

def _to_str(value: bytes):
    return value.decode('utf-8' , 'ignore') if isinstance(value , bytes) else value

class filesystem:
    __list_files = wrap_function('list_files', [c_char_p], c_void_p)
    __size_c = wrap_function('size', [c_void_p], c_int)
    __get_data_c = wrap_function('get_data', [c_void_p, c_int], c_char_p)
    __free_memory = wrap_function('free_memory', [c_void_p])
    @staticmethod
    def list_files(path: Union[str, Path]):
        try:
            files = []
            vector = filesystem.__list_files(to_byte_str(path))
        except OSError:
            print(f"{path} doesn't exist.")
            return []
        else:
            for i in range(filesystem.__size(vector)):
                files.append(filesystem.__get_data(vector, i))
        finally:
            filesystem.__free_memory(vector)
            return files

    @staticmethod
    def __size(vector):
        return filesystem.__size_c(vector)

    @staticmethod
    def __get_data(vector, idx: int):
        return _to_str(filesystem.__get_data_c(vector, idx))

if __name__ == '__main__':
    for f in filesystem.list_files('.'):
        print(f)