// api/products.js — Vercel Serverless Function
const fs   = require('fs');
const path = require('path');

const DB_PATH   = path.join('/tmp', 'products.json');
const SEED_PATH = path.join(process.cwd(), 'products.json');
const ADMIN_TOKEN = process.env.ADMIN_TOKEN;

function loadDB() {
    if (fs.existsSync(DB_PATH)) {
        return JSON.parse(fs.readFileSync(DB_PATH, 'utf8'));
    }
    return JSON.parse(fs.readFileSync(SEED_PATH, 'utf8'));
}

function saveDB(data) {
    fs.writeFileSync(DB_PATH, JSON.stringify(data, null, 2), 'utf8');
}

module.exports = (req, res) => {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

    if (req.method === 'OPTIONS') return res.status(200).end();

    // GET — вернуть все товары
    if (req.method === 'GET') {
        try {
            return res.status(200).json(loadDB());
        } catch(e) {
            return res.status(500).json({ error: 'Ошибка загрузки' });
        }
    }

    // POST — сохранить товары
    if (req.method === 'POST') {
        const auth  = req.headers['authorization'] || '';
        const token = auth.replace('Bearer ', '').trim();

        if (!ADMIN_TOKEN || token !== ADMIN_TOKEN) {
            return res.status(401).json({ error: 'Неверный токен' });
        }

        try {
            const data = req.body;
            if (typeof data !== 'object' || Array.isArray(data)) {
                return res.status(400).json({ error: 'Неверный формат' });
            }
            saveDB(data);
            return res.status(200).json({ ok: true, count: Object.keys(data).length });
        } catch(e) {
            return res.status(500).json({ error: 'Ошибка сохранения: ' + e.message });
        }
    }

    return res.status(405).json({ error: 'Метод не поддерживается' });
};
