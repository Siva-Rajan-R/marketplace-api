from typing import TypedDict,Optional


class ResponseContentTypDict(TypedDict):
    status:int
    succsess:bool
    msg:str
    description:Optional[str]