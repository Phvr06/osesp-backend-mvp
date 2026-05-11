from typing import List, Dict, Any

# Listas em memória simulando as tabelas
concerts_db: List[Dict[str, Any]] = []
users_db: List[Dict[str, Any]] = []

# Contadores para simular o ID auto-incremental
concert_id_counter = 1
user_id_counter = 1