# Edge Case Scenarios

| Scenario                          | Action Taken                          |
|----------------------------------|----------------------------------------|
| Forked prompt is deleted         | Label original as "(deleted)"          |
| Session crashed mid-reply        | Mark as `incomplete` and retry export  |
| 10+ failed PIN attempts in 1hr   | Flag as abuse, notify SuperAdmin       |
| Same IP, 200 sessions in 5min    | CAPTCHA trigger, IP cooldown           |
