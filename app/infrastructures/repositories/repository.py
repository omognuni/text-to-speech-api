from typing import Callable, ContextManager, Tuple
from sqlalchemy.orm import Session

from abc import ABC, abstractmethod

from domains.entities import Model

class AbstractRepository(ABC):
    
    @abstractmethod
    def __init__(self, model: Model, session_factory: Callable[..., ContextManager[Session]], media_root: str = '') -> None:
        self.model = model
        self.session_factory = session_factory
        self.media_root = media_root
    
    @abstractmethod
    def get_all(self)-> list:
        pass
    
    @abstractmethod
    def get_or_create(self, **kwargs)-> Tuple:
        pass

    @abstractmethod
    def get_by_id(self, instance_id: int)-> Model:
        pass
    
    @abstractmethod
    def add(self, **kwargs)-> Model:
        pass
        
    @abstractmethod
    def update(self, instance_id: int, **kwargs)-> Model:
        pass

    @abstractmethod
    def delete(self, instance_id: int)-> None:
        pass



class AbstractMediaRepository(ABC):
    
    def __init__(self):
        pass