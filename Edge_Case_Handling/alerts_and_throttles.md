# Alerts & Throttling Logic

- CAPTCHA Trigger:
  - 3+ sessions in <10s by same IP
  - 10+ failed PINs within 5 minutes
- Alert Escalation:
  - System logs to SuperAdmin webhook
  - Alert bell on Admin panel header
