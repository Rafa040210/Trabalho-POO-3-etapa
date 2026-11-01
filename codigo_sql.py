from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table
from sqlalchemy import select, update, delete, insert, func, asc, desc
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

engine = create_engine('sqlite:///escola.db')

## Código inspirado no trabalho anterior só que sem a implementação do boletim(não sabia como fazer :( !)

### criando as tabelas
Base = declarative_base()

class Turma(Base):
    __tablename__ = 'turmas'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    tipo = Column(String)

    Alunos = relationship('Aluno', back_populates='turma_objeto')

    #Relação N:N com professor
    Professores = relationship('Professor', secondary='siapes', back_populates='turmas')

    def __repr__(self):
        return f"Turma({self.id}, {self.nome})"

class Aluno(Base):
    __tablename__ = 'aluno'
    matricula = Column(Integer, primary_key=True, autoincrement=False)
    nome = Column(String)
    sexo = Column(String)
    curso = Column(String)

    turma_id = Column(
      Integer, ForeignKey('turmas.id') )

    turma_objeto = relationship('Turma', back_populates='Alunos')

    def __repr__(self):
        return f"Aluno({self.matricula}, {self.nome}, {self.curso})"


class Professor(Base):
    __tablename__ = 'professor'
    siape = Column(Integer, primary_key=True, autoincrement=False)
    nome = Column(String)
    formacao = Column(String)

    relationship('Turma', secondary='siapes', back_populates='Professores')

    def __repr__(self):
        return f"Professor({self.siape}, {self.nome})"


siapes = Table(
    'siapes', Base.metadata,
    Column('professor_siape', Integer, ForeignKey('professor.siape'), primary_key=True),
    Column('turma_id', Integer, ForeignKey('turmas.id'), primary_key=True)
)



Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)



## Inserindo os dados nas tabelas
Session = sessionmaker(bind=engine)
session = Session()

#Inserindo dados na tabela turma

Infomatica_1A = Turma(nome='Informática 1A', tipo='Informática')

Infomatica_2A = Turma(nome='Informática 2A', tipo='Informática')


Infomatica_3A = Turma(nome='Informática 3A', tipo='Informática')


Eletro_1 = Turma(nome='Eletro 1', tipo='Eletro')
Eletro_2 = Turma(nome='Eletro 2', tipo='Eletro')
Eletro_3 = Turma(nome='Eletro 3', tipo='Eletro')

Administracao_1A = Turma(nome='Administração 1A', tipo='Administração')

Administracao_2A = Turma(nome='Administração 2A', tipo='Administração')

Administracao_3A = Turma(nome='Administração 3A', tipo='Administração')

#Inserindo dados na tabela aluno
#vou inserir um por um

al1 = Aluno(matricula=12345, nome='Luara Santos', sexo='Feminino', curso='Administração',  turma_objeto=Administracao_2A)

al2 = Aluno(matricula=10356, nome='Mariana Merike', sexo='Feminino', curso='Administração',  turma_objeto=Administracao_2A)

al3 = Aluno(matricula=19340, nome='Raika Sousa', sexo='Feminino', curso='Administração',  turma_objeto=Administracao_3A)


al4 = Aluno(matricula=17395, nome='Katarina Souares', sexo='Feminino', curso='Administração',  turma_objeto=Administracao_1A)

al5 = Aluno(matricula=18845, nome='Katarina Oliveira', sexo='Feminino', curso='Informática', turma_objeto=Infomatica_1A)

al6 = Aluno(matricula=12399, nome='Deigo Dias Oliveira', sexo='Masculino', curso='Informática', turma_objeto=Infomatica_3A)

al7 = Aluno(matricula=10045, nome='Luiz Martiz', sexo='Masculino', data_nas='2008-09-20', curso='Informática',  turma_objeto=Infomatica_3A)

al8 = Aluno(matricula=18945, nome='Luiz Sousa', sexo='Masculino', curso='Informática', turma_objeto=Infomatica_1A)

al9 = Aluno(matricula=12234, nome='Lucas Soares', sexo='Masculino', curso='Informática', turma_objeto=Infomatica_2A)

al10 = Aluno(matricula=12900, nome='Lucas Oliveira', sexo='Masculino', curso='Eletro', turma_objeto=Eletro_1)


al11 = Aluno(matricula=15345, nome='Matheus Alves Dias', sexo='Masculino', curso='Eletro', turma_objeto=Eletro_1)


al12 = Aluno(matricula=12205, nome='Matheus Gonçalves', sexo='Masculino', curso='Eletro', turma_objeto=Eletro_2)


al13 = Aluno(matricula=13340, nome='Juan Dias', sexo='Masculino', curso='Eletro', turma_objeto=Eletro_3)

#Inserindo dados N:N
#Tabela professor

Ana = Professor(siape=1234, nome='Ana Mariana de Sousa', formacao='Biologia')

Diego = Professor(siape=1345, nome='Diego Martiz Soares da cunha', formacao='Química')

Luiza = Professor(siape=3444, nome='Luiza Dias Silva', formacao='Banco de Dados')

Felipe = Professor(siape=5432, nome='Felipe Cunha Sauro', formacao='Máquinas Elétricas')

Renata = Professor(siape=1321, nome='Renata de Marta Silva', formacao='Empreendedorismo')

Solange = Professor(siape=7654, nome='Solange Maria dos Anjos', formacao='Artes' )

#Mandando para o BD

session.add_all([Ana, Diego, Luiza, Felipe, Renata, Solange, al1, al2, al3, al4, al5, al6, al7, al8, al9, al10, al11, al12, al13, Infomatica_1A, Infomatica_2A, Infomatica_3A, Eletro_1, Eletro_2, Eletro_3, Administracao_1A, Administracao_2A, Administracao_3A  ])

#Inserindo dados na tabela associativa

session.execute(siapes.insert(), [
    {"professor_siape": 1234, "turma_id": 1},
    {"professor_siape": 1234, "turma_id": 4},
    {"professor_siape": 1345, "turma_id": 1},
    {"professor_siape": 1345, "turma_id": 8},
    {"professor_siape": 1345, "turma_id": 9},
    {"professor_siape": 3444, "turma_id": 1},
    {"professor_siape": 3444, "turma_id": 2},
    {"professor_siape": 3444, "turma_id": 3},
    {"professor_siape": 5432, "turma_id": 5},
    {"professor_siape": 5432, "turma_id": 6},
    {"professor_siape": 5432, "turma_id": 4},
    {"professor_siape": 1321, "turma_id": 7},
    {"professor_siape": 1321, "turma_id": 8},
    {"professor_siape": 1321, "turma_id": 9},
    {"professor_siape": 7654, "turma_id": 6},
    {"professor_siape": 7654, "turma_id": 7},
    {"professor_siape": 7654, "turma_id": 5}
] )   

session.commit()


