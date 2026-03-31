require('dotenv').config();

const { createApp } = require('./config/app_factory');

const PORT = process.env.PORT || 5000;

async function main() {
  const app = await createApp();
  
  app.listen(PORT, '0.0.0.0', () => {
    console.log(`Server running on port ${PORT}`);
  });
}

main().catch(err => {
  console.error('Failed to start server:', err);
  process.exit(1);
});
