# Stage 1: Build the React application
FROM node:18-slim AS build

WORKDIR /app

# Copy package.json and package-lock.json
COPY promptwise-ui/package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY promptwise-ui/ .

# Build the application
RUN npm run build

# Stage 2: Serve the application with Nginx
FROM nginx:alpine

# Copy the build output to Nginx's default content directory
COPY --from=build /app/dist /usr/share/nginx/html

# Copy a custom nginx configuration to handle React Router
COPY promptwise-ui/nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
