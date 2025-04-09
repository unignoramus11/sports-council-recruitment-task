FROM node:18-alpine

WORKDIR /app

# Install dependencies (with package.json)
COPY package*.json ./
RUN npm install

# Copy local code to the container
COPY . .

# Set environment to development
ENV NODE_ENV=development

# Expose port for development server
EXPOSE 5173

# Start the development server
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]