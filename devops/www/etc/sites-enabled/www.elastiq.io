upstream uwsgi {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    index index.html;

    location /static/ {
        root /opt/elastiq/assets;
    }

    location / {
        proxy_set_header X-Real-IP      $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_pass http://uwsgi;
        proxy_set_header Host $http_host;
    }
}
