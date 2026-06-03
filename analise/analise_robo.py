import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

# ===================== CONFIGURAÇÕES =====================
plt.style.use('seaborn-v0_8')

def analisar_dados(csv_path):
    try:
        df = pd.read_csv(csv_path)
        print("✅ Arquivo carregado com sucesso!\n")
    except Exception as e:
        print(f"❌ Erro ao ler o CSV: {e}")
        return

    # ==================== ANÁLISE =====================
    print("="*60)
    print("📊 ANÁLISE DO ROBÔ SEGUIDOR DE LINHA")
    print("="*60)
    
    tempo_total = df['tempo_ms'].max() / 1000.0
    print(f"⏱️  Tempo total da corrida : {tempo_total:.1f} segundos")
    print(f"📏 Distância estimada     : {df['vel_kmh'].mean() * tempo_total / 3.6:.2f} metros")
    print(f"⚡ Velocidade média       : {df['vel_kmh'].mean():.2f} km/h")
    print(f"📉 Erro médio             : {df['erro'].mean():.2f}")
    print(f"📈 Oscilação (std do erro): {df['erro'].std():.2f}")
    print(f"🔢 Número de amostras     : {len(df)}")
    print("="*60)

    # ==================== GRÁFICOS =====================
    fig = plt.figure(figsize=(14, 10))

    # Gráfico 1: Erro ao longo do tempo
    plt.subplot(2, 2, 1)
    plt.plot(df['tempo_ms']/1000, df['erro'], 'b-', linewidth=1.5)
    plt.axhline(0, color='r', linestyle='--', alpha=0.7)
    plt.title('Erro x Tempo')
    plt.xlabel('Tempo (segundos)')
    plt.ylabel('Erro')
    plt.grid(True)

    # Gráfico 2: Velocidade
    plt.subplot(2, 2, 2)
    plt.plot(df['tempo_ms']/1000, df['vel_kmh'], 'g-', linewidth=2)
    plt.title('Velocidade Estimada x Tempo')
    plt.xlabel('Tempo (segundos)')
    plt.ylabel('Velocidade (km/h)')
    plt.grid(True)

    # Gráfico 3: PWM dos motores
    plt.subplot(2, 2, 3)
    plt.plot(df['tempo_ms']/1000, df['pwm_esq'], label='Motor Esquerdo', color='orange')
    plt.plot(df['tempo_ms']/1000, df['pwm_dir'], label='Motor Direito', color='blue')
    plt.title('PWM dos Motores')
    plt.xlabel('Tempo (segundos)')
    plt.ylabel('PWM')
    plt.legend()
    plt.grid(True)

    # Gráfico 4: RPM
    plt.subplot(2, 2, 4)
    plt.plot(df['tempo_ms']/1000, df['rpm'], 'r-', linewidth=1.5)
    plt.title('RPM x Tempo')
    plt.xlabel('Tempo (segundos)')
    plt.ylabel('RPM')
    plt.grid(True)

    plt.tight_layout()
    plt.show()

    # Salvar gráficos
    plt.savefig('analise_robo.png', dpi=300, bbox_inches='tight')
    print("💾 Gráfico salvo como 'analise_robo.png'")

# ===================== EXECUÇÃO =====================
if __name__ == "__main__":
    if len(sys.argv) > 1:
        arquivo = sys.argv[1]
    else:
        arquivo = "data.csv"
    
    if not os.path.exists(arquivo):
        print(f"❌ Arquivo '{arquivo}' não encontrado!")
        print("Coloque o arquivo data.csv na mesma pasta ou passe o caminho como argumento.")
    else:
        analisar_dados(arquivo)