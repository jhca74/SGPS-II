import os
import subprocess
from datetime import datetime

def git_commit_push(mensagem="Atualização automática via script"):
    try:
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        commit_msg = f"{mensagem} ({data})"

        print("🔄 A preparar alterações para commit...")
        subprocess.run(["git", "add", "."], check=True)

        print("📝 A fazer commit...")
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)

        print("🚀 A enviar para o GitHub...")
        subprocess.run(["git", "push", "origin", "main"], check=True)

        print("✅ Commit e push concluídos com sucesso!")

    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar: {e}")
    except Exception as erro:
        print(f"❌ Erro inesperado: {erro}")

if __name__ == "__main__":
    git_commit_push("Atualização automática da Sara")
