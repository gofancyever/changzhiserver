from model.models import ChangzhiServerSection,Base,ChangzhiServerNewsModel
from model.config import engine

Base.metadata.create_all(engine) #创建表结构
