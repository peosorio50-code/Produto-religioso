#!/usr/bin/env bash
# Monta entregas/novena-pelos-filhos.zip: um zip só, com pastas (sem zip dentro de zip). Uso: bash filhos/montar_zip.sh
set -euo pipefail
RAIZ=$(cd "$(dirname "$0")/.." && pwd)
TMP=$(mktemp -d); P="$TMP/novena-pelos-filhos"
mkdir -p "$P/servidor" "$P/docs" "$P/roteiros/capas-dos-videos"
cp "$RAIZ/filhos/roteiros/00-LEIA-PRIMEIRO-CARLOS.md" "$P/00-LEIA-PRIMEIRO.md"
cp "$RAIZ"/filhos/docs/*.md "$P/docs/"
cp "$RAIZ"/filhos/roteiros/0[1-9]-*.md "$P/roteiros/"
cp "$RAIZ"/filhos/site/img/dia*.jpg "$RAIZ/filhos/site/img/terco.jpg" "$RAIZ/filhos/site/img/vsl-capa.jpg" "$RAIZ"/filhos/site/img/amostra-*.jpg "$P/roteiros/capas-dos-videos/"
(cd "$RAIZ/servidor" && cp -r servidor.py filhos.py filhos_conteudo.py filhos_pdf.py filhos_fontes \
                              casamento.py casamento_conteudo.py casamento_pdf.py casamento_fontes "$P/servidor/")
cp -r "$RAIZ/filhos/site" "$P/site"
cp -r "$RAIZ/filhos/kit/kiwify" "$RAIZ/filhos/kit/criativos" "$RAIZ/filhos/kit/exemplos" "$P/"
find "$P" -name '__pycache__' -prune -exec rm -rf {} +
find "$P" \( -name '.env' -o -name '.DS_Store' -o -name '*.pyc' \) -delete
rm -f "$RAIZ/entregas/novena-pelos-filhos.zip"
(cd "$TMP" && zip -qr "$RAIZ/entregas/novena-pelos-filhos.zip" novena-pelos-filhos)
rm -rf "$TMP"
echo "ok: entregas/novena-pelos-filhos.zip"
