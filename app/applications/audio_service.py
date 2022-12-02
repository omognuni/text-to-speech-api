class BaseService:
    
    def __init__(self, repository) -> None:
        self._repository = repository
        
    def get_objects(self):
        return self._repository.get_all()
    
    def get_object_by_id(self, object_id: int):
        return self._repository.get_by_id(object_id)
    
    def create(self, **kwargs):
        return self._repository.add(**kwargs)
    
    def get_or_create(self, **kwargs):
        return self._repository.get_or_create(**kwargs)
    
    def update(self, **kwargs):
        return self._repository.update(**kwargs)
    
    def delete(self, object_id):
        return self._repository.delete(object_id)


class ProjectService(BaseService):
    pass

class AudioService(BaseService):
    pass
    
class AudioTextService(BaseService):
    
    def insert(self, index: int, content: list, audio_id: list):
        return self._repository.insert(index, content, audio_id)
