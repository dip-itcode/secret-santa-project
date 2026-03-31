require('dotenv').config();

const express = require('express');
const cors = require('cors');
const apiRoutes = require('../routes/api_routes');
const { MongoService } = require('../services/mongo_service');

async function createApp(config = {}) {
  const app = express();

  const debug = config.DEBUG || process.env.DEBUG === 'true';
  const mongoUri = config.MONGO_URI || process.env.MONGO_URI || '';

  app.use(cors());
  app.use(express.json());
  app.use(express.urlencoded({ extended: true }));

  if (mongoUri) {
    try {
      const mongo = new MongoService(mongoUri);
      const connected = await mongo.connect();
      if (connected) {
        apiRoutes.setMongoService(mongo);
        console.log('MongoDB connected ✅');
      } else {
        console.warn('MongoDB ping failed — running without DB');
      }
    } catch (exc) {
      console.warn(`MongoDB init failed: ${exc.message}`);
    }
  }

  app.use('/api', apiRoutes);

  app.use((req, res) => {
    res.status(404).json({ error: 'Not found' });
  });

  app.use((err, req, res, next) => {
    console.error('Unhandled error:', err);
    res.status(500).json({ error: 'Internal server error' });
  });

  return app;
}

module.exports = { createApp };
