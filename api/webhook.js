export default async function handler(req, res) {
  if (req.method === 'POST') {
    let payload = req.body;
    
    if (typeof payload === 'string') {
      try {
        payload = JSON.parse(payload);
      } catch (e) {
        console.error("❌ JSON 파싱 실패:", e);
        return res.status(400).json({ error: "잘못된 JSON 형식" });
      }
    }

    console.log("📥 웹훅 수신:", payload);

    // TODO: GPT 분석 호출 가능
    // await sendToGPT(payload);

    res.status(200).json({ message: '웹훅 수신 완료' });
  } else {
    res.status(405).json({ message: '허용되지 않은 메서드' });
  }
}
