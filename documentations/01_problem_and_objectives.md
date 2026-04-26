# 01 - Problem and Objectives

## Domain Context
Modern water treatment facilities rely on interconnected industrial control systems (ICS) and IoT sensors. This connectivity increases exposure to cyber threats, including false data injection, command tampering, and stealthy attacks that resemble normal operational behavior.

## Problem Statement
Detect anomalies and cyber-attacks in real time from multivariate sensor streams while:
- Preserving system availability
- Minimizing false alarms
- Meeting strict low-latency constraints

## Key Challenges
- High dimensional, heterogeneous sensor features
- Strong dependencies between process stages
- Similarity between attack patterns and legitimate operating changes
- Real-time detection requirements
- Operational reliability constraints

## Project Objectives
- Build anomaly detection models for SWaT-like process data
- Maximize attack detection capability (high recall)
- Keep precision acceptable to reduce false shutdowns
- Prepare an architecture suitable for production deployment

## Scope in Current Repository
Current implementation focuses on:
- Data preparation and feature engineering
- Offline model training and evaluation
- Exporting model artifacts and preprocessed datasets

Cloud deployment, API serving, alerting, and MLOps automation are planned next-phase activities.
