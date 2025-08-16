# Prompt Lifecycle Notes

## 🧠 Design Considerations

- Forking a prompt should duplicate the structure, but reset status to "draft"
- Only Admins can delete an approved prompt
- Editors can request review but cannot self-approve
- Rejected prompts remain visible to creator with comments

## ❓ Open Questions

- Can the same prompt title exist under multiple creators?
- Should forks inherit tags or start clean?
