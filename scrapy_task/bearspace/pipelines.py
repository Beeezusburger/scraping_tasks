import pandas as pd


class BearspacePipeline(object):
    def __init__(self, crawler):
        self.buffer = []

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_item(self, item, spider):
        self.buffer.append(item)
        return item

    def close_spider(self, spider):
        df = pd.DataFrame.from_records(self.buffer)
        print(df)