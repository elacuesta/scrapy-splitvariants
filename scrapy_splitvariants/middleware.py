from copy import deepcopy
from scrapy.item import DictItem
from scrapy.exceptions import NotConfigured


class SplitVariantsMiddleware(object):

    variants_key = 'variants'  # default value

    def __init__(self, variants_key):
        if variants_key:
            self.variants_key = variants_key

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool("SPLITVARIANTS_ENABLED"):
            raise NotConfigured
        variants_key = crawler.settings.get("SPLITVARIANTS_KEY")
        return cls(variants_key)

    def process_spider_output(self, response, result, spider):
        for r in result:
            if isinstance(r, (DictItem, dict)) and self.variants_key in r:
                variants = r.pop(self.variants_key)
                for variant in variants:
                    new_product = deepcopy(r)
                    new_product.update(variant)
                    yield new_product
            else:
                yield r
