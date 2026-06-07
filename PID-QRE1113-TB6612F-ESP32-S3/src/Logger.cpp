#include "Logger.h"

Logger logger;

void Logger::begin() {
    startTime = millis();
    lastLog = millis();
    logs.reserve(800);
    Serial.println("\n=== LOGGER INICIADO - Seguidor de Linha ===\n");
    Serial.println("tempo_ms,rpm,vel_kmh,erro,correcao_pid,pwm_esq,pwm_dir");
}

void Logger::log(int erro, float correcao, int pwmE, int pwmD, float kp, float ki_term, float kd_term, float rpmVal) {
    if (millis() - lastLog < 80) return;

    float deltaT = (millis() - lastLog) / 1000.0f;
    float velInstant = ((abs(pwmE) + abs(pwmD)) / 2.0f) * 0.0018f;
    distancia += velInstant * deltaT;

    LogEntry entry;
    entry.tempo = millis() - startTime;
    entry.rpm = rpmVal;
    entry.velKmh = rpmVal * 0.018;
    entry.erro = erro;
    entry.correcaoPID = correcao;
    entry.pwmEsq = pwmE;
    entry.pwmDir = pwmD;
    entry.kp_term = kp;
    entry.ki_term = ki_term;
    entry.kd_term = kd_term;

    logs.push_back(entry);
    Serial.printf("%lu,%.1f,%.2f,%d,%.1f,%d,%d\n",
        entry.tempo, entry.rpm, entry.velKmh, entry.erro,
        entry.correcaoPID, entry.pwmEsq, entry.pwmDir);

    lastLog = millis();
}

void Logger::endRun() {
    Serial.println("\n=== FIM DA CORRIDA - DADOS COLETADOS ===\n");
    printStats();
    saveToSerialCSV();
}

void Logger::printStats() {
    Serial.printf("Tempo total      : %.1f segundos\n", getTempoTotal());
    Serial.printf("Distância        : %.2f metros\n", distancia);
    Serial.printf("Velocidade média : %.2f km/h\n", getVelMedia());
    Serial.printf("Amostras         : %d\n", logs.size());
}

void Logger::saveToSerialCSV() {
    Serial.println("\n--- COLE TODO ESTE CONTEÚDO ABAIXO EM UM ARQUIVO data.csv ---");
    Serial.println("tempo_ms,rpm,vel_kmh,erro,correcao_pid,pwm_esq,pwm_dir");
    for (auto& e : logs) {
        Serial.printf("%lu,%.1f,%.2f,%d,%.1f,%d,%d\n",
            e.tempo, e.rpm, e.velKmh, e.erro, e.correcaoPID, e.pwmEsq, e.pwmDir);
    }
}

float Logger::getVelMedia() {
    float t = getTempoTotal();
    return (t > 0) ? (distancia / t) * 3.6f : 0;
}

float Logger::getTempoTotal() {
    return (millis() - startTime) / 1000.0f;
}

void Logger::reset() {
    logs.clear();
    distancia = 0;
    startTime = millis();
}