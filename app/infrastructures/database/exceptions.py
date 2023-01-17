class NotFoundError(Exception):
    
    def __init__(self, entity_id):
        super().__init__(f"not found, id: {entity_id}")