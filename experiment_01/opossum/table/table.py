import pandas
from collections import deque


class Table:
    def __init__(self, data):
        if isinstance(data, pandas.DataFrame):
            self.data = data

        elif isinstance(data, Table):
            self.data = data.data

        elif isinstance(data, pandas.Series):
            self.data = pandas.DataFrame(data)

        else:
            self.data = pandas.api.interchange.from_dataframe(data, allow_copy=True)

    def __getitem__(self, transforms):
        cls = self.__class__

        if not isinstance(transforms, (tuple, list)):
            transforms = [transforms]
            
        transforms = deque(transforms)
        data = self.data
        
        while transforms:
            transform = transforms.popleft()
            
            if isinstance(transform, list):
                transforms.extendleft(reversed(transform))
                continue

            data = cls(transform(data)).data

        return cls(data)

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        return self.data.__repr__()

    def _repr_html_(self):
        return self.data._repr_html_()

    def __dataframe__(self, nan_as_null=False, allow_copy=True):
        return self.data.__dataframe__(nan_as_null=nan_as_null, allow_copy=allow_copy)
