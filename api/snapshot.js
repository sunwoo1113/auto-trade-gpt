// pages/api/snapshot.js
import fs from 'fs';
import path from 'path';

export default async function handler(req, res) {
  if (req.method === 'POST') {
    const snapshot = req.body;
    const filePath = path.join(process.cwd(), 'logs', `snapshot_${Date.now()}.json`);
    fs.mkdirSync(path.dirname(filePath), { recursive: true });
    fs.writeFileSync(filePath, JSON.stringify(snapshot, null, 2));
    res.status(200).json({ message: 'Snapshot saved' });
  } else {
    res.status(405).json({ message: 'Method not allowed' });
  }
}
