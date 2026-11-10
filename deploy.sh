#!/usr/bin/env bash
# Despliega o reinicia todo: Mosquitto, API y consumer.
# Uso:  ./deploy.sh            -> git pull + rebuild + reinicio
#       ./deploy.sh --no-pull  -> solo rebuild + reinicio (sin traer cambios)

set -euo pipefail

main() {
    cd "$(dirname "$(readlink -f "$0")")"

    if [[ ! -f .env ]]; then
        echo "✗ No existe .env en $(pwd)"; exit 1
    fi

    if [[ "${1:-}" != "--no-pull" ]]; then
        echo "→ Trayendo cambios del repo..."
        git pull --ff-only
    fi

    echo "→ Construyendo imagen cs1-api..."
    docker build -q -t cs1-api . > /dev/null

    echo "→ Levantando Mosquitto..."
    docker compose up -d

    echo "→ Reiniciando API y consumer..."
    docker rm -f cs1-api cs1-consumer > /dev/null 2>&1 || true

    docker run -d --name cs1-api --restart unless-stopped \
        --env-file .env \
        -p 127.0.0.1:5000:5000 \
        -v cs1-models:/app/app/models_files \
        cs1-api > /dev/null

    echo -n "→ Esperando a la API"
    for _ in $(seq 1 60); do
        if curl -fs http://127.0.0.1:5000/health > /dev/null; then
            echo " ✓"
            break
        fi
        echo -n "."
        sleep 2
    done
    if ! curl -fs http://127.0.0.1:5000/health > /dev/null; then
        echo " ✗ La API no respondió. Logs:"
        docker logs --tail 30 cs1-api
        exit 1
    fi

    docker run -d --name cs1-consumer --restart unless-stopped \
        --env-file .env \
        --network host \
        cs1-api python -m app.consumer > /dev/null

    docker image prune -f > /dev/null

    echo
    docker ps --filter "name=cs1-" --format "table {{.Names}}\t{{.Status}}"
    echo
    echo "✓ Listo"
}

# Todo va dentro de main para que un git pull que modifique este archivo
# no rompa la ejecución en curso.
main "$@"