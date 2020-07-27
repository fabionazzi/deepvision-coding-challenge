# Use nginx image
FROM nginx

# Remove default config file
RUN rm /etc/nginx/conf.d/default.conf

# Replace with our own config file
COPY nginx.conf /etc/nginx/conf.d/nginx.conf
