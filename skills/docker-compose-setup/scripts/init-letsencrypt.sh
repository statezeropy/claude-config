#!/bin/bash

# Let's Encrypt SSL certificate automation script
# Usage: sudo ./init-letsencrypt.sh domain.com [--staging]

if [ -z "$1" ]; then
    echo "❌ Usage: $0 domain.com [--staging]"
    exit 1
fi

domains=($1)
email="admin@yourdomain.com"  # Change this
staging=0

if [ "$2" = "--staging" ]; then
    staging=1
fi

rsa_key_size=4096
data_path="./certbot"
compose_file="docker-compose.yml"

echo "============================================================"
echo "🔐 Let's Encrypt SSL Certificate"
echo "============================================================"
echo "📧 Email: $email"
echo "🌐 Domain: ${domains[@]}"
echo "🧪 Mode: $([ $staging = 1 ] && echo 'STAGING' || echo 'PRODUCTION')"
echo "============================================================"
echo

# Step 1: Create dummy certificate
for domain in "${domains[@]}"; do
    domain_path="$data_path/conf/live/$domain"
    echo "🔧 Creating dummy certificate for $domain..."
    mkdir -p "$domain_path"
    
    if [ ! -f "$domain_path/privkey.pem" ]; then
        openssl req -x509 -nodes -newkey rsa:$rsa_key_size -days 1 \
            -keyout "$domain_path/privkey.pem" \
            -out "$domain_path/fullchain.pem" \
            -subj "/CN=localhost" 2>/dev/null
        echo "✅ Dummy certificate created"
    fi
done
echo

# Step 2: Start nginx
echo "🚀 Starting nginx..."
docker compose -f "$compose_file" up -d nginx
echo "✅ Nginx started"
echo

# Step 3: Delete dummy certificate
for domain in "${domains[@]}"; do
    echo "🗑️  Deleting dummy certificate..."
    rm -rf "$data_path/conf/live/$domain"
done
echo

# Step 4: Request Let's Encrypt certificate
echo "📜 Requesting Let's Encrypt certificate..."

staging_arg=""
if [ $staging != "0" ]; then
    staging_arg="--staging"
    echo "⚠️  STAGING mode (test certificate)"
else
    echo "✅ PRODUCTION mode (real certificate)"
fi

docker compose -f "$compose_file" run --rm certbot certonly \
    --webroot \
    --webroot-path=/var/www/certbot \
    $staging_arg \
    --email $email \
    --agree-tos \
    --no-eff-email \
    --force-renewal \
    $(printf -- "-d %s " "${domains[@]}")

if [ $? -eq 0 ]; then
    echo "✅ Certificate obtained for ${domains[@]}"
else
    echo "❌ Certificate request failed"
    exit 1
fi
echo

# Step 5: Reload nginx
echo "🔄 Reloading nginx..."
docker compose -f "$compose_file" exec nginx nginx -s reload
echo "✅ Nginx reloaded"
echo

echo "============================================================"
echo "✅ Setup completed!"
echo "============================================================"

if [ $staging != "0" ]; then
    echo "⚠️  STAGING certificates are for testing only"
    echo "Run again without --staging for production"
else
    echo "🎉 Production certificates active!"
    echo "Verify: https://$domain"
fi
echo "============================================================"

