# AutoTune Architecture

```text
React Dashboard
      |
      v
FastAPI REST API
      |
+-----+---------+----------+
|               |          |
v               v          v
Monitoring       ML    Optimization
|               |          |
v               v          v
psutil       RandomForest  State
|               |          |
+---------------+----------+
                |
                v
              SQLite
```

Data flow:
1. Monitoring collects performance metrics.
2. ML estimates high-load probability.
3. Optimizer applies predefined application-level strategies.
4. Recovery restores normal configuration when load returns to normal.
5. SQLite stores telemetry and optimization events.
