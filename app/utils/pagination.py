from typing import List, Any

class PaginationParams:
    def __init__(self, page: int = 1, page_size: int = 10):
        self.page = page
        self.page_size = page_size

def paginate_results(results: List[Any], page: int, page_size: int) -> List[Any]:
    start = (page - 1) * page_size
    end = start + page_size
    return results[start:end]