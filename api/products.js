// api/products.js — Vercel Serverless Function
const fs   = require('fs');
const path = require('path');

const DB_PATH    = path.join('/tmp', 'products.json');
const SEED_PATH  = path.join(process.cwd(), 'products.json');
const ADMIN_TOKEN = process.env.ADMIN_TOKEN || '';

function loadDB() {
    try {
        if (fs.existsSync(DB_PATH)) return JSON.parse(fs.readFileSync(DB_PATH, 'utf8'));
        return JSON.parse(fs.readFileSync(SEED_PATH, 'utf8'));
    } catch(e) {
        return {};
    }
}

function saveDB(data) {
    fs.writeFileSync(DB_PATH, JSON.stringify(data, null, 2), 'utf8');
}

// Parse body manually (Vercel doesn't always auto-parse)
function parseBody(req) {
    return new Promise((resolve) => {
        if (req.body) return resolve(req.body);
        let body = '';
        req.on('data', chunk => { body += chunk.toString(); });
        req.on('end', () => {
            try { resolve(JSON.parse(body)); }
            catch(e) { resolve({}); }
        });
    });
}

module.exports = async (req, res) => {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

    if (req.method === 'OPTIONS') return res.status(200).end();

    if (req.method === 'GET') {
        return res.status(200).json(loadDB());
    }

    if (req.method === 'POST') {
        const auth  = (req.headers['authorization'] || '').replace('Bearer ', '').trim();

        // Debug: return what we received (remove after fix)
        if (auth === 'debug') {
            return res.status(200).json({
                received_token: auth,
                env_token_set: !!ADMIN_TOKEN,
                env_token_length: ADMIN_TOKEN.length
            });
        }

        if (!ADMIN_TOKEN || auth !== ADMIN_TOKEN) {
            return res.status(401).json({
                error: 'Неверный токен',
                hint: 'Проверьте ADMIN_TOKEN в Vercel Environment Variables'
            });
        }

        try {
            const data = await parseBody(req);
            saveDB(data);
            return res.status(200).json({ ok: true, count: Object.keys(data).length });
        } catch(e) {
            return res.status(500).json({ error: e.message });
        }
    }

    return res.status(405).end();
};
