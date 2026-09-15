import os
import psycopg
from dataclasses import dataclass
from typing import Optional

@dataclass
class ClienteDB:
    id: str
    nome: str
    cpf: str
    email: str
    status: str

def buscar_cliente_por_cpf(cpf: str, db_url: Optional[str] = None) -> Optional[ClienteDB]:
    url = db_url or os.getenv("DATABASE_URL")
    if not url:
        return None

    # Normalizar prefixo se vier no formato SQLAlchemy (postgresql+psycopg:// -> postgresql://)
    if url.startswith("postgresql+psycopg://"):
        url = url.replace("postgresql+psycopg://", "postgresql://")
    elif url.startswith("postgresql+pg8000://"):
        url = url.replace("postgresql+pg8000://", "postgresql://")

    with psycopg.connect(url) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, nome, cpf, email, status FROM clientes WHERE cpf = %s LIMIT 1",
                (cpf,)
            )
            row = cur.fetchone()
            if row:
                return ClienteDB(
                    id=str(row[0]),
                    nome=str(row[1]),
                    cpf=str(row[2]),
                    email=str(row[3]),
                    status=str(row[4])
                )
    return None
