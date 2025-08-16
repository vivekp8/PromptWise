# PIN Lockout Logic

- Max PIN attempts: 3 per 24 hours
- After 3 failures:
  - Lock account for 12 hours
  - Admin override required for unlock
- PINs hashed at rest using bcrypt (`bcrypt(p, salt)`)
- Audit log generated for every PIN entry attempt
