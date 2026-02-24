class GraphElement:
    def __init__(self, id, **kwargs):
        self.id = id
        self.data = kwargs

    def __getitem__(self, key):
        return self.data.get(key)
    
    def __setitem__(self, key, value):
        if key == 'id':
            return 
        
        self.data[key] = value

    def get_attribute(self, key):
        return self.data.get(key)
    
    def update(self, **data):
        if 'id' in data:
            del data['id']

        self.data.update(data)