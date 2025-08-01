
from sqlalchemy import Column,Integer,String,Float
from sqlalchemy.orm import declarative_base


Base=declarative_base()

class Students(Base):
    __tablename__='users'
    id=Column(Integer,primary_key=True,autoincrement=True,nullable=False)
    Admission=Column(Integer,nullable=False)
    Course=Column(Integer,nullable=False)
    Unit=Column(Integer,nullable=False)

    def __init__(self,Admission,Course,Unit):
        self.Admission=Admission
        self.Course=Course
        self.Unit=Unit
    