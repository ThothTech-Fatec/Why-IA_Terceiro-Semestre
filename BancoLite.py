import sqlite3

conn = sqlite3.connect('farmacia.db', timeout=10)
cursor = conn.cursor()

# Removendo as tabelas se já existirem
cursor.execute('DROP TABLE IF EXISTS carrinho')
cursor.execute('DROP TABLE IF EXISTS medicamentos')

# Criando a tabela medicamentos
cursor.execute('''
CREATE TABLE IF NOT EXISTS medicamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    descricao TEXT,
    formula TEXT,
    preco REAL NOT NULL,
    precisa_receita BOOLEAN NOT NULL CHECK (precisa_receita IN (0, 1)),
    sintomas TEXT,
    quantidade_estoque INTEGER NOT NULL
)
''')

# Criando a tabela carrinho
cursor.execute('''
CREATE TABLE IF NOT EXISTS carrinho (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    medicamento_id INTEGER NOT NULL,
    quantidade_no_carrinho INTEGER NOT NULL,
    FOREIGN KEY (medicamento_id) REFERENCES medicamentos(id)
)
''')

# Medicamentos para inserção na tabela
medicamentos = [
    ('Paracetamol', 'Analgésico e antipirético', 'C8H9NO2', 4.50, 0, 'Febre, dor de cabeça', 150),
    ('Ibuprofeno', 'Anti-inflamatório não esteroide', 'C13H18O2', 10.00, 0, 'Inflamações, dor, febre', 80),
    ('Amoxicilina', 'Antibiótico', 'C16H19N3O5S', 12.99, 1, 'Infecções bacterianas', 30),
    ('Lorazepam', 'Ansiolítico', 'C15H10Cl2N2O2', 20.00, 1, 'Ansiedade', 25),
    ('Omeprazol', 'Inibidor da bomba de prótons', 'C17H19N3O3S', 15.50, 0, 'Refluxo, gastrite', 60),
    ('Diclofenaco', 'Anti-inflamatório', 'C14H11Cl2NO2', 8.75, 0, 'Dor, inflamação', 40),
    ('Simeticona', 'Antiflatulento', 'C6H18O4Si3', 6.30, 0, 'Gases', 120),
    ('Ranitidina', 'Antiácido', 'C13H22N4O3', 13.50, 0, 'Úlcera, azia', 70),
    ('Cetirizina', 'Antialérgico', 'C21H25ClN2O3', 9.00, 0, 'Alergias', 90),
    ('Losartana', 'Antihipertensivo', 'C22H23ClN6O', 18.00, 1, 'Pressão alta', 50),
    ('Metformina', 'Antidiabético', 'C4H11N5', 10.00, 1, 'Diabetes tipo 2', 60),
    ('Simvastatina', 'Redutor de colesterol', 'C25H38O5', 12.00, 1, 'Colesterol alto', 75),
    ('Salbutamol', 'Broncodilatador', 'C13H21NO3', 14.50, 1, 'Asma, bronquite', 45),
    ('Clonazepam', 'Ansiolítico', 'C15H10ClN3O3', 22.50, 1, 'Ansiedade, epilepsia', 35),
    ('Amitriptilina', 'Antidepressivo', 'C20H23N', 17.00, 1, 'Depressão, dor crônica', 40),
    ('Dipirona', 'Analgésico e antitérmico', 'C13H16N3NaO4S', 5.00, 0, 'Febre, dor', 200),
    ('Fluoxetina', 'Antidepressivo', 'C17H18F3NO', 25.00, 1, 'Depressão, ansiedade', 30),
    ('Prednisona', 'Corticosteroide', 'C21H26O5', 15.00, 1, 'Inflamação', 55),
    ('Enalapril', 'Antihipertensivo', 'C20H28N2O5', 8.50, 1, 'Pressão alta', 80),
    ('Cloridrato de Ciprofloxacino', 'Antibiótico', 'C17H18FN3O3', 18.00, 1, 'Infecções bacterianas', 20),
    ('Cloroquina', 'Antimalárico', 'C18H26ClN3', 16.50, 1, 'Malária, doenças autoimunes', 15),
    ('Albendazol', 'Anti-helmíntico', 'C12H15N3O2S', 7.50, 0, 'Vermes, parasitas', 90),
    ('Hidroxicloroquina', 'Antimalárico e anti-inflamatório', 'C18H26ClN3O', 28.00, 1, 'Malária, doenças autoimunes', 25),
    ('Espinoractona', 'Diurético', 'C24H32O4S', 19.75, 1, 'Retenção de líquidos, hipertensão', 40),
    ('Fenobarbital', 'Anticonvulsivante', 'C12H12N2O3', 20.00, 1, 'Convulsões', 18),
    ('Azitromicina', 'Antibiótico', 'C38H72N2O12', 15.50, 1, 'Infecções bacterianas', 25),
    ('Bromoprida', 'Antiemético', 'C14H22BrN3O2', 8.50, 0, 'Náusea, vômito', 110),
    ('Atenolol', 'Antihipertensivo', 'C14H22N2O3', 9.50, 1, 'Pressão alta, angina', 60),
    ('Levodopa', 'Antiparkinsoniano', 'C9H11NO4', 30.00, 1, 'Parkinson', 15),
    ('Metoclopramida', 'Antiemético e pró-cinético', 'C14H22ClN3O2', 6.75, 0, 'Náusea, refluxo', 100)
]

# Inserindo medicamentos na tabela
cursor.executemany('''
    INSERT INTO medicamentos (nome, descricao, formula, preco, precisa_receita, sintomas, quantidade_estoque)
    VALUES (?, ?, ?, ?, ?, ?, ?)
''', medicamentos)

# Salvando as alterações e fechando a conexão
conn.commit()
conn.close()
