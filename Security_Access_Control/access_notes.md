# Access Notes

## 🎯 Questions

- Should PINs expire or rotate every 90 days?
- Can one SuperAdmin downgrade another? Conflict rules?

## 🧠 Design Insights

- PINs are one-time for elevation — never reused
- Guests have no access to protected routes even via URL
- Audit logs must record internal API calls too (e.g. CRONs)
