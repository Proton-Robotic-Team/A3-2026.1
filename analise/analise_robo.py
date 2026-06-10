import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

plt.style.use('default')

def analisar_dados(csv_path):
    try:
        df = pd.read_csv(csv_path)
        print(f"✅ Arquivo carregado: {len(df)} linhas\n")
    except Exception as e:
        print(f"❌ Erro ao ler CSV: {e}")
        return

    print("="*70)
    print("📊 ANÁLISE DO ROBÔ SEGUIDOR DE LINHA")
    print("="*70)
    
    tempo_total = df['tempo_ms'].max() / 1000.0
    vel_media = df['vel_kmh'].mean()
    
    print(f"⏱️  Tempo total          : {tempo_total:.1f} segundos")
    print(f"📏 Distância estimada   : {(vel_media * tempo_total / 3.6):.2f} metros")
    print(f"⚡ Velocidade média     : {vel_media:.2f} km/h")
    print(f"📉 Erro médio           : {df['erro'].mean():.2f}")
    print(f"📈 Oscilação            : {df['erro'].std():.2f}")
    print("="*70)

    # ==================== GRÁFICOS MELHORADOS =====================
    fig = plt.figure(figsize=(15, 11), constrained_layout=True)

    # Gráfico 1: Erro
    ax1 = fig.add_subplot(2, 2, 1)
    ax1.plot(df['tempo_ms']/1000, df['erro'], 'b-', linewidth=1.8)
    ax1.axhline(0, color='r', linestyle='--', alpha=0.8)
    ax1.set_title('Erro ao longo do Tempo', fontsize=12, pad=10)
    ax1.set_xlabel('Tempo (segundos)')
    ax1.set_ylabel('Erro')
    ax1.grid(True)

    # Gráfico 2: Velocidade
    ax2 = fig.add_subplot(2, 2, 2)
    ax2.plot(df['tempo_ms']/1000, df['vel_kmh'], 'g-', linewidth=2)
    ax2.set_title('Velocidade Estimada x Tempo', fontsize=12, pad=10)
    ax2.set_xlabel('Tempo (segundos)')
    ax2.set_ylabel('Velocidade (km/h)')
    ax2.grid(True)

    # Gráfico 3: PWM
    ax3 = fig.add_subplot(2, 2, 3)
    ax3.plot(df['tempo_ms']/1000, df['pwm_esq'], label='Esquerdo', color='orange', linewidth=1.5)
    ax3.plot(df['tempo_ms']/1000, df['pwm_dir'], label='Direito', color='blue', linewidth=1.5)
    ax3.set_title('PWM dos Motores', fontsize=12, pad=10)
    ax3.set_xlabel('Tempo (segundos)')
    ax3.set_ylabel('PWM')
    ax3.legend()
    ax3.grid(True)

    # Gráfico 4: RPM
    ax4 = fig.add_subplot(2, 2, 4)
    ax4.plot(df['tempo_ms']/1000, df['rpm'], 'r-', linewidth=1.8)
    ax4.set_title('RPM x Tempo', fontsize=12, pad=10)
    ax4.set_xlabel('Tempo (segundos)')
    ax4.set_ylabel('RPM')
    ax4.grid(True)

    # Salvar ANTES de mostrar
    plt.savefig('analise_robo.png', dpi=300, bbox_inches='tight')
    print("💾 Gráfico salvo como 'analise_robo.png' (alta qualidade)")

    plt.show()


# ===================== EXECUÇÃO =====================
if __name__ == "__main__":
    possiveis = ["data.csv", "analise/data.csv", "../data.csv"]
    
    arquivo = None
    for p in possiveis:
        if os.path.exists(p):
            arquivo = p
            break
    
    if not arquivo:
        csv_files = [f for f in os.listdir('.') if f.lower().endswith('.csv')]
        if csv_files:
            arquivo = csv_files[0]
    
    if not arquivo:
        print("❌ Nenhum arquivo .csv encontrado!")
        sys.exit(1)

    print(f"🔍 Analisando: {arquivo}\n")
    analisar_dados(arquivo)