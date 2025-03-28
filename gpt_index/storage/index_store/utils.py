from gpt_index.constants import DATA_KEY, TYPE_KEY
from gpt_index.data_structs.data_structs_v2 import V2IndexStruct
from gpt_index.data_structs.registry import INDEX_STRUCT_TYPE_TO_INDEX_STRUCT_CLASS


def index_struct_to_json(index_struct: V2IndexStruct) -> dict:
    index_struct_dict = {
        TYPE_KEY: index_struct.get_type(),
        DATA_KEY: index_struct.to_dict(),
    }
    return index_struct_dict


def json_to_index_struct(struct_dict: dict) -> V2IndexStruct:
    type = struct_dict[TYPE_KEY]
    data_dict = struct_dict[DATA_KEY]
    cls = INDEX_STRUCT_TYPE_TO_INDEX_STRUCT_CLASS[type]
    return cls.from_dict(data_dict)
