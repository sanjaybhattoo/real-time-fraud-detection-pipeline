# real-time-fraud-detection-pipeline
Data engineering project that demonstrates event-driven architecture, real-time stream processing, and microservices design in production grade environment.

Goal :
1. project capacity upto 100k+ per sec 
2. 400ms for transaction to fraud detection. 

Technologies used : Python, Go, Node.js, Docker, Kubernetes, Kafka, PostgreSQL, Redis .

System architecture followed : 




<img width="663" height="585" alt="Screenshot 2026-03-07 at 1 57 10 AM" src="https://github.com/user-attachments/assets/a7b105dc-c975-45b1-8363-05d91042cfb3" />


Steps followed by me to implement this end to end : 

1. Project setup and Docker setup
2. Database schema design
3. Kafka setup - clusters and topics
4. Services :
       a. Transaction processor
       b. Feature enigine
       c. --working on ---



Goal : Latency timeline expected :

<img width="1283" height="117" alt="Screenshot 2026-03-07 at 2 10 08 AM" src="https://github.com/user-attachments/assets/956108f1-64dd-417b-8033-b993299b6a03" />


Can be scaled using combination of : Kafka partitioning + stateless microservices + Kubernetes HPA + databases
