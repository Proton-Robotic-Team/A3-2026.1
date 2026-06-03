#pragma once
#include <Arduino.h>
#include <vector>
#include "PID.h"
#include "Motores.h"

struct LogEntry {
    unsigned long tempo;
    float rpm;
    float velKmh;
    int erro;
    float correcaoPID;
    int pwmEsq;
    int pwmDir;
    float kp_term;
    float ki_term;
    float kd_term;
};

class Logger {
private:
    std::vector<LogEntry> logs;
    unsigned long lastLog = 0;
    unsigned long startTime = 0;
    float distancia = 0.0f;

public:
    void begin();
    void log(int erro, float correcao, int pwmE, int pwmD);
    void endRun();
    void printStats();
    void saveToSerialCSV();
    void reset();
    
    float getVelMedia();
    float getTempoTotal();
};

extern Logger logger;