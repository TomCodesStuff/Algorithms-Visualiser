from enum import Enum

class ScreenType(Enum):
    MAIN_MENU = "main_menu"
    SEARCH = "search"
    SORT = "sort"
    TRAVERSAL = "traversal"


class SortDirection(Enum):
    ASCENDING = 0
    DESCENDING = 1