# Backup & Restore

## Backup

```bash
curl -s -u admin:admin http://rabbitmq-192.168.0.100.nip.io/api/definitions | jq > definitions.json
```

## restore

```bash
curl -X POST -H "Content-Type: application/json" -u admin:admin -d @definitions.json http://rabbitmq-192.168.0.100.nip.io/api/definitions
```
