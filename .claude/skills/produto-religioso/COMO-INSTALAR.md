# Como instalar a skill "produto-religioso"

**No seu Mac (vale para todos os repositórios no Claude Code):**
```
mkdir -p ~/.claude/skills && unzip -o skill-produto-religioso.zip -d ~/.claude/skills
```
Depois, abra o Claude Code em qualquer pasta e peça, por exemplo: "use a skill produto-religioso e monte um produto novo". Também dá para chamar direto com `/produto-religioso`.

**Num repositório específico (vale também nas sessões na nuvem do claude.ai/code):** copie a pasta `produto-religioso` para `.claude/skills/` dentro do repositório e faça o commit.

**Para atualizar:** troque a pasta inteira pela versão nova (por exemplo, quando o manual do Meu Santo mudar, substitua `references/manual-meu-santo-protetor.md`).
