import React, { useState } from "react"; // React와 useState 훅을 가져옵니다.
import axios from "axios"; // axios는 HTTP 요청을 보내기 위해 사용됩니다.
import { GoogleLogin } from "@react-oauth/google"; // GoogleLogin 컴포넌트를 가져옵니다.

const EstrusDashboard = () => {
  // result는 발정 감지 결과를 저장하기 위한 상태입니다.
  const [result, setResult] = useState(null);
  // userToken은 구글 로그인 후 받은 액세스 토큰을 저장하는 상태입니다.
  const [userToken, setUserToken] = useState(null);

  // 발정 감지 함수
  const detectEstrus = async () => {
    try {
      const response = await axios.post("http://localhost:8000/api/v1/estrus/", {
        cow_id: "1", // CharField에 맞춰 문자열로
        // cctv_source: "http://example.com/cctv/video.mp4" // 모델의 cctv_source 필드 사용
      });
      setResult(response.data.prediction);
    } catch (error) {
      console.error("Error:", error.response ? error.response.data : error.message);
      setResult("오류 발생: " + (error.response ? JSON.stringify(error.response.data) : error.message));
    }
  };

  // Google 로그인 성공 처리 함수
  const handleLoginSuccess = (response) => {
    const token = response.credential;
    setUserToken(token); // 로그인 성공 시 액세스 토큰을 상태에 저장

    // 서버에 로그인 토큰을 전송하는 로직
    fetch("http://your-backend-url/api/auth/google", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ token }),
    })
      .then((res) => res.json())
      .then((data) => {
        // 서버에서 받은 데이터 처리
        console.log(data);
      })
      .catch((error) => {
        console.error("Google login error", error);
      });
  };

  // Google 로그인 실패 처리 함수
  const handleLoginError = () => {
    console.log("Login failed");
  };

  return (
    <div>
      {/* 구글 로그인 버튼 */}
      <GoogleLogin
        onSuccess={handleLoginSuccess}
        onError={handleLoginError}
      />

      {/* 로그인 후 사용자가 발정 감지 버튼을 클릭할 수 있도록 버튼 제공 */}
      {userToken && (
        <div>
          <button onClick={detectEstrus}>발정 감지</button>
        </div>
      )}

      {/* 결과가 있을 경우 결과를 화면에 표시 */}
      {result && <p>결과: {JSON.stringify(result)}</p>}
    </div>
  );
};

export default EstrusDashboard;
