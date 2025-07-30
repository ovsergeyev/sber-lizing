from urllib.parse import urlparse, parse_qs

class Pagination:
    def __init__(self):
        self.all_links = set()
        self.processed_links = set()
        
    def add_links(self, links: list[str]):
        self.all_links = self.all_links.union(set(links))
        
    def _get_page_num(self, link):
        query = urlparse(link).query
        params = parse_qs(query)
        return int(params.get("PAGEN_1", [0])[0])
        
    def get_link(self):
        remaining_links = self.all_links - self.processed_links
        if not remaining_links:
            return None
        sorted_links = sorted(remaining_links, key=self._get_page_num, reverse=True)
        link = sorted_links.pop()
        self.processed_links.add(link)
        return link