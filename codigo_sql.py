from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table, Float
from sqlalchemy import select, update, delete, insert, func, asc, desc
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

engine = create_engine('sqlite:///escola.db')


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


    # Atalho: Não cria coluna no banco, mas posso fazer `aluno.boletins` 

    boletins = relationship('Boletim', back_populates='aluno')


        
class Boletim(Base):
    __tablename__ = 'boletim'
    id = Column(Integer, primary_key=True) 
    disciplina = Column(String(50))        
    nota = Column(Float)   

    aluno_matricula = Column(Integer, ForeignKey('aluno.matricula'))

    aluno = relationship('Aluno', back_populates='boletins')


class Professor(Base):
    __tablename__ = 'professor'
    siape = Column(Integer, primary_key=True, autoincrement=False)
    nome = Column(String)
    formacao = Column(String)

    turmas = relationship('Turma', secondary='siapes', back_populates='Professores')

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

al1 = Aluno(matricula=12345, nome='Luara Santos', sexo='Feminino', curso='Administração', turma_objeto=Administracao_2A)

al2 = Aluno(matricula=10356, nome='Mariana Merike', sexo='Feminino', curso='Administração', turma_objeto=Administracao_2A)

al3 = Aluno(matricula=19340, nome='Raika Sousa', sexo='Feminino', curso='Administração', turma_objeto=Administracao_3A)


al4 = Aluno(matricula=17395, nome='Katarina Souares', sexo='Feminino', curso='Administração', turma_objeto=Administracao_1A)

al5 = Aluno(matricula=18845, nome='Katarina Oliveira', sexo='Feminino', curso='Informática', turma_objeto=Infomatica_1A)

al6 = Aluno(matricula=12399, nome='Deigo Dias Oliveira', sexo='Masculino', curso='Informática', turma_objeto=Infomatica_3A)

al7 = Aluno(matricula=10045, nome='Luiz Martiz', sexo='Masculino', curso='Informática',  turma_objeto=Infomatica_3A)

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
    {"professor_siape": 1234, "turma_id": 4}, #okk
    {"professor_siape": 1345, "turma_id": 1},
    {"professor_siape": 1345, "turma_id": 8},
    {"professor_siape": 1345, "turma_id": 9}, #okk
    {"professor_siape": 3444, "turma_id": 1},
    {"professor_siape": 3444, "turma_id": 2},
    {"professor_siape": 3444, "turma_id": 3}, #okk
    {"professor_siape": 5432, "turma_id": 5},
    {"professor_siape": 5432, "turma_id": 6},
    {"professor_siape": 5432, "turma_id": 4}, #okk
    {"professor_siape": 1321, "turma_id": 7},
    {"professor_siape": 1321, "turma_id": 8},
    {"professor_siape": 1321, "turma_id": 9}, #okk
    {"professor_siape": 7654, "turma_id": 6},
    {"professor_siape": 7654, "turma_id": 7},
    {"professor_siape": 7654, "turma_id": 5}
] )   


Notas_Luara_Santos = [
    Boletim(aluno_matricula=12345, disciplina='Química', nota=7.0), #okk
    Boletim(aluno_matricula=12345, disciplina='Empreendedorismo', nota=2.5), #okk
]

Notas_Mariana = [
      Boletim(aluno_matricula=10356, disciplina='Química', nota=7.9), #okk
      Boletim(aluno_matricula=10356, disciplina='Empreendedorismo', nota=4.5), #okk
]

Notas_Raika = [
      Boletim(aluno_matricula=19340, disciplina='Química', nota=3.4), #okk
      Boletim(aluno_matricula=19340, disciplina='Empreendedorismo', nota=10.0), #okk
]

Notas_Katarina = [
      Boletim(aluno_matricula=17395, disciplina='Biologia', nota=9.5), #okk
      Boletim(aluno_matricula=17395, disciplina='Artes', nota=8.0), #okk
      Boletim(aluno_matricula=17395, disciplina='Empreendedorismo', nota=9.0), #Ok
]

Notas_Katarina_Oliveira = Boletim(aluno_matricula=18845, disciplina='Banco de Dados', nota=7.5), #ok


Notas_Deigo = Boletim(aluno_matricula=12399, disciplina='Banco de Dados', nota=5.5), #ok


Notas_Luiz_Martiz = Boletim(aluno_matricula=10045, disciplina='Banco de Dados', nota=1.4), #ok

Notas_Luiz_Sousa = [
      Boletim(aluno_matricula=18945, disciplina='Biologia', nota=7.0), #Okk
      Boletim(aluno_matricula=18945, disciplina='Banco de Dados', nota=8.0), #ok
]

Notas_Lucas = Boletim(aluno_matricula=12234, disciplina='Banco de Dados', nota=10.0), #ok


Notas_Lucas_Oliveira = [
      Boletim(aluno_matricula=12900, disciplina='Biologia', nota=2.7), #okk
      Boletim(aluno_matricula=12900, disciplina='Máquinas Elétricas', nota=1.6), #ok
]
    

Notas_Matheus = [
      Boletim(aluno_matricula=15345, disciplina='Biologia', nota=6.5), #okk
      Boletim(aluno_matricula=15345, disciplina='Máquinas Elétricas', nota=6.0), #okk
]

Notas_Matheus_Gonçalves = [
      Boletim(aluno_matricula=12205, disciplina='Artes', nota=7.8), #okk
      Boletim(aluno_matricula=12205, disciplina='Máquinas Elétricas', nota=5.7), #okk
]

Notas_Juan = [
      Boletim(aluno_matricula=13340, disciplina='Artes', nota=5.0), #okk
      Boletim(aluno_matricula=12205, disciplina='Máquinas Elétricas', nota=5.9), #okk
]

# Dá erro se fizer asim session.add_all([Notas_Luara_Santos, Notas_Mariana, Notas_Deigo, Notas_Juan, Notas_Katarina, Notas_Katarina_Oliveira, Notas_Lucas, Notas_Lucas_Oliveira, Notas_Luiz_Martiz, Notas_Matheus, Notas_Matheus_Gonçalves, Notas_Luiz_Sousa, Notas_Raika])
#Vou fazer assim:
todas_as_listas = [
    Notas_Luara_Santos, Notas_Mariana, Notas_Deigo, Notas_Juan, 
    Notas_Katarina, Notas_Katarina_Oliveira, Notas_Lucas, Notas_Lucas_Oliveira, 
    Notas_Luiz_Martiz, Notas_Matheus, Notas_Matheus_Gonçalves, Notas_Luiz_Sousa, Notas_Raika
]

for lista_aluno in todas_as_listas:
    for nota in lista_aluno:
        session.add(nota)
        
session.commit()


