# -*- coding: utf-8 -*-
from enum import Enum


class Tags(str, Enum):
    DOCUMENTS = "documents"
    DYNAMIC = "dynamic"
    FILES = "files"
    LANGCHAIN = "langchain"
    SPLITTERS = "splitters"
    TEXT = "text"
