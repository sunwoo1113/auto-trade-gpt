export default async function handler(req, res) {
  if (req.method === 'POST') {
    const payload = req.body;
    
    // 받은 신호 로그 출력 또는 저장
    console.log("📥 웹훅 수신:", payload);

    // 예시: GPT 분석 요청 준비 (여기선 생략)
    // await sendToGPT(payload);

    res.status(200).json({ message: '웹훅 수신 완료' });
  } else {
    res.status(405).json({ message: '허용되지 않은 메서드' });
  }
}
