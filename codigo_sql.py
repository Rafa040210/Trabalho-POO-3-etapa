from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table
from sqlalchemy import select, update, delete, insert, func, asc, desc
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

engine = create_engine('sqlite:///escola.db')

## Código inspirado no trabalho anterior só que sem a implementação do boletim(não sabia como fazer :( !)

### criando as tabelas
Base = declarative_base()

siapes = Table(
    'siapes', Base.metadata,
    Column('professor_siape', Integer, ForeignKey('professores.siape'), primary_key=True),
    Column('turma_id', Integer, ForeignKey('turmas.id'), primary_key=True)
)

class Turma(Base):
    __tablename__ = 'turma'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    tipo = Column(String)

    Alunos = relationship('Aluno', back_populates='turma')

    #Relação N:N com professor
    Professores = relationship('Professor', secondary=siapes, back_populates='turmas')

    def __repr__(self):
        return f"Turma({self.id}, {self.nome})"

class Aluno(Base):
    __tablename__ = 'aluno'
    matricula = Column(Integer, primary_key=True)
    nome = Column(String)
    sexo = Column(String)
    data_nas = Column(Date)
    curso = Column(String)
    periodo = Column(String)

    #um aluno só tem uma turma

    Turmas = relationship('Turma', back_populates='aluno')

    def __repr__(self):
        return f"Aluno({self.matricula}, {self.nome}, {self.curso})"


class Professor(Base):
    __tablename__ = 'professor'
    siape = Column(Integer, primary_key=True)
    nome = Column(String)
    formacao = Column(String)
    data_nas = Column(Date)


    turmas = relationship('turma', secondary=siapes, back_populates='professores') #chave estrangeira

    def __repr__(self):
        return f"Professor({self.siape}, {self.nome})"



Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)



## Inserindo os dados nas tabelas

